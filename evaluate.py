"""
Evaluation script for the Mental Health Care System
"""

import sys
import os
import asyncio
import pandas as pd
import nest_asyncio
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import (
    BatchEvalRunner,
    CorrectnessEvaluator,
    FaithfulnessEvaluator,
    RelevancyEvaluator
)
from llama_index.core.llama_dataset.generator import RagDatasetGenerator
import openai

from src.ingest_pipeline import ingest_documents
from src.index_builder import build_indexes
from src.global_settings import DEFAULT_MODEL, DEFAULT_TEMPERATURE, SIMILARITY_TOP_K

# Apply nested asyncio
nest_asyncio.apply()


def initialize_settings(api_key):
    """Initialize OpenAI settings"""
    openai.api_key = api_key
    Settings.llm = OpenAI(model=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE)


def generate_questions(nodes, num_questions_per_chunk=1):
    """Generate evaluation questions from nodes"""
    print(f"\nGenerating questions from {len(nodes)} nodes...")
    dataset_generator = RagDatasetGenerator(
        nodes, 
        num_questions_per_chunk=num_questions_per_chunk
    )
    eval_questions = dataset_generator.generate_questions_from_nodes()
    df = eval_questions.to_pandas()
    print(f"✓ Generated {len(df)} questions")
    return df


async def evaluate_async(query_engine, df):
    """Run async evaluation"""
    print("\nRunning evaluation...")
    
    correctness_evaluator = CorrectnessEvaluator()
    faithfulness_evaluator = FaithfulnessEvaluator()
    relevancy_evaluator = RelevancyEvaluator()
    
    runner = BatchEvalRunner(
        {
            "correctness": correctness_evaluator,
            "faithfulness": faithfulness_evaluator,
            "relevancy": relevancy_evaluator
        },
        show_progress=True
    )
    
    eval_result = await runner.aevaluate_queries(
        query_engine=query_engine,
        queries=[question for question in df['query']],
    )
    
    return eval_result


def aggregate_results(df, eval_result):
    """Aggregate evaluation results"""
    print("\nAggregating results...")
    data = []
    
    for i, question in enumerate(df['query']):
        correctness_result = eval_result['correctness'][i]
        faithfulness_result = eval_result['faithfulness'][i]
        relevancy_result = eval_result['relevancy'][i]
        
        data.append({
            'Query': question,
            'Correctness_response': correctness_result.response,
            'Correctness_passing': correctness_result.passing,
            'Correctness_feedback': correctness_result.feedback,
            'Correctness_score': correctness_result.score,
            'Faithfulness_response': faithfulness_result.response,
            'Faithfulness_passing': faithfulness_result.passing,
            'Faithfulness_feedback': faithfulness_result.feedback,
            'Faithfulness_score': faithfulness_result.score,
            'Relevancy_response': relevancy_result.response,
            'Relevancy_passing': relevancy_result.passing,
            'Relevancy_feedback': relevancy_result.feedback,
            'Relevancy_score': relevancy_result.score,
        })
    
    df_result = pd.DataFrame(data)
    return df_result


def print_and_save_scores(df_result):
    """Print and save average scores"""
    correctness_scores = df_result['Correctness_score'].mean()
    faithfulness_scores = df_result['Faithfulness_score'].mean()
    relevancy_scores = df_result['Relevancy_score'].mean()
    
    print("\n" + "=" * 50)
    print("EVALUATION RESULTS")
    print("=" * 50)
    print(f"Correctness scores:  {correctness_scores:.4f}")
    print(f"Faithfulness scores: {faithfulness_scores:.4f}")
    print(f"Relevancy scores:    {relevancy_scores:.4f}")
    print("=" * 50)
    
    # Save results
    os.makedirs("eval_results", exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save detailed results
    df_result.to_csv(
        f"eval_results/evaluation_results_{timestamp}.csv", 
        index=False, 
        encoding='utf-8-sig'
    )
    print(f"\n✓ Detailed results saved to: eval_results/evaluation_results_{timestamp}.csv")
    
    # Save summary
    with open(f"eval_results/average_scores_{timestamp}.txt", "w", encoding='utf-8') as f:
        f.write(f"Evaluation Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        f.write(f"Correctness scores:  {correctness_scores:.4f}\n")
        f.write(f"Faithfulness scores: {faithfulness_scores:.4f}\n")
        f.write(f"Relevancy scores:    {relevancy_scores:.4f}\n")
    print(f"✓ Summary saved to: eval_results/average_scores_{timestamp}.txt")
    
    return correctness_scores, faithfulness_scores, relevancy_scores


def main():
    """Main evaluation function"""
    print("=" * 50)
    print("Mental Health Care System - Evaluation")
    print("=" * 50)
    
    # Get API key
    api_key = input("\nEnter your OpenAI API key: ").strip()
    if not api_key:
        print("Error: API key is required!")
        return
    
    # Initialize
    print("\n[1/5] Initializing settings...")
    initialize_settings(api_key)
    print("✓ Settings initialized")
    
    # Load nodes
    print("\n[2/5] Loading documents and creating nodes...")
    nodes = ingest_documents()
    print(f"✓ Loaded {len(nodes)} nodes")
    
    # Build index
    print("\n[3/5] Building index...")
    index = build_indexes(nodes)
    query_engine = index.as_query_engine(similarity_top_k=SIMILARITY_TOP_K)
    print("✓ Index and query engine created")
    
    # Generate questions
    print("\n[4/5] Generating evaluation questions...")
    df_questions = generate_questions(nodes, num_questions_per_chunk=1)
    
    # Save questions
    os.makedirs("eval_results", exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    df_questions.to_csv(
        f"eval_results/evaluation_questions_{timestamp}.csv",
        index=False,
        encoding='utf-8-sig'
    )
    print(f"✓ Questions saved to: eval_results/evaluation_questions_{timestamp}.csv")
    
    # Run evaluation
    print("\n[5/5] Running evaluation...")
    eval_result = asyncio.run(evaluate_async(query_engine, df_questions))
    df_result = aggregate_results(df_questions, eval_result)
    
    # Print and save scores
    print_and_save_scores(df_result)
    
    print("\n" + "=" * 50)
    print("Evaluation completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()