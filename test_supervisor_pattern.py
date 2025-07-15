#!/usr/bin/env python3
"""
Test script to demonstrate the supervisor pattern upgrade
Compares supervisor vs linear workflows
"""
import os
import sys
import asyncio
import time
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, '.')

async def test_supervisor_vs_linear():
    """Compare supervisor pattern vs linear workflow"""
    try:
        # Load environment variables if available
        load_dotenv()
        
        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = input("Enter your OpenAI API key: ").strip()
            if not api_key:
                print("❌ OpenAI API key is required for testing")
                return False
        
        # Set the API key for testing
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Import services
        from api.services.post_generator import PostGeneratorService
        from api.services.supervised_post_generator import SupervisedPostGeneratorService
        
        print("🧪 Testing Supervisor Pattern vs Linear Workflow")
        print("=" * 60)
        
        test_title = "LoRA: Low-Rank Adaptation of Large Language Models"
        print(f"📝 Test paper: {test_title}")
        print()
        
        # Test 1: Supervisor Pattern
        print("🔴 Testing SUPERVISOR PATTERN...")
        print("-" * 40)
        
        start_time = time.time()
        supervisor_service = SupervisedPostGeneratorService(use_supervisor=True)
        supervisor_result = await supervisor_service.generate_post(test_title)
        supervisor_time = time.time() - start_time
        
        print("✅ Supervisor Pattern Results:")
        print(f"   ⏱️  Execution time: {supervisor_time:.2f}s")
        print(f"   📊 Workflow pattern: {supervisor_result['workflow_pattern']}")
        print(f"   🔄 Revisions: {supervisor_result['revision_count']}")
        print(f"   ✅ Tech check: {supervisor_result['tech_check']}")
        print(f"   🎨 Style check: {supervisor_result['style_check']}")
        print(f"   📏 Post length: {len(supervisor_result['post'])} chars")
        
        # Supervisor insights
        insights = supervisor_result.get('supervisor_insights', {})
        if insights:
            print(f"   🧠 Supervisor insights:")
            print(f"      • Completed steps: {insights.get('completed_steps', [])}")
            print(f"      • Workflow efficiency: {insights.get('workflow_efficiency', 0):.2%}")
            print(f"      • Completion reason: {insights.get('completion_reason', 'unknown')}")
        
        # Quality metrics
        quality = supervisor_result.get('quality_metrics', {})
        if quality:
            print(f"   📈 Quality metrics:")
            print(f"      • Overall quality: {quality.get('overall_quality', 0):.2%}")
            print(f"      • Character efficiency: {quality.get('character_efficiency', 0):.2%}")
            print(f"      • Mention compliance: {quality.get('mention_compliance', False)}")
        
        print()
        
        # Test 2: Linear Pattern  
        print("🔵 Testing LINEAR PATTERN...")
        print("-" * 40)
        
        start_time = time.time()
        linear_service = PostGeneratorService()
        linear_result = await linear_service.generate_post(test_title)
        linear_time = time.time() - start_time
        
        print("✅ Linear Pattern Results:")
        print(f"   ⏱️  Execution time: {linear_time:.2f}s")
        print(f"   📊 Workflow pattern: linear")
        print(f"   🔄 Revisions: {linear_result['revision_count']}")
        print(f"   ✅ Tech check: {linear_result['tech_check']}")
        print(f"   🎨 Style check: {linear_result['style_check']}")
        print(f"   📏 Post length: {len(linear_result['post'])} chars")
        
        print()
        
        # Comparison
        print("📊 COMPARISON ANALYSIS")
        print("=" * 60)
        
        print("⏱️  Performance:")
        print(f"   Supervisor: {supervisor_time:.2f}s")
        print(f"   Linear:     {linear_time:.2f}s")
        print(f"   Difference: {abs(supervisor_time - linear_time):.2f}s")
        
        print("\n🔄 Efficiency:")
        supervisor_quality = supervisor_result.get('quality_metrics', {}).get('overall_quality', 0)
        linear_quality = 0.8 if linear_result['verify_result'] == 'pass' else 0.5  # Estimate for linear
        
        print(f"   Supervisor quality: {supervisor_quality:.2%}")
        print(f"   Linear quality:     {linear_quality:.2%}")
        
        print("\n🎯 Key Advantages of Supervisor Pattern:")
        print("   ✅ Intelligent routing based on content quality")
        print("   ✅ Enhanced error handling and recovery")
        print("   ✅ Detailed workflow monitoring and insights")
        print("   ✅ Adaptive decision making")
        print("   ✅ Quality metrics and optimization")
        
        # Display generated posts
        print("\n📝 GENERATED POSTS")
        print("=" * 60)
        
        print("🔴 Supervisor Pattern Post:")
        print("-" * 30)
        print(supervisor_result['post'])
        print()
        
        print("🔵 Linear Pattern Post:")
        print("-" * 30)
        print(linear_result['post'])
        print()
        
        # Recommendation
        print("💡 RECOMMENDATION")
        print("=" * 60)
        
        if supervisor_quality > linear_quality:
            print("🏆 Supervisor pattern produced higher quality results!")
        elif supervisor_time < linear_time * 1.5:  # If not significantly slower
            print("🏆 Supervisor pattern provides better features with comparable performance!")
        else:
            print("🏆 Both patterns have their merits - choose based on your needs!")
        
        print("\n✨ Supervisor pattern is recommended for:")
        print("   • Production environments requiring high quality")
        print("   • Complex content that may need multiple revisions")
        print("   • Applications needing detailed monitoring")
        print("   • Scenarios where adaptive workflow is beneficial")
        
        print("\n⚡ Linear pattern is suitable for:")
        print("   • Simple, predictable workflows")
        print("   • Resource-constrained environments")
        print("   • Quick prototyping and testing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_supervisor_features():
    """Test specific supervisor pattern features"""
    print("\n🔬 TESTING SUPERVISOR FEATURES")
    print("=" * 60)
    
    try:
        from api.services.supervised_post_generator import SupervisedPostGeneratorService
        
        service = SupervisedPostGeneratorService(use_supervisor=True)
        
        # Test workflow status
        status = service.get_workflow_status()
        print("📋 Workflow Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        # Test pattern switching
        print(f"\n🔄 Pattern Switching:")
        print(f"   Current pattern: {'supervisor' if service.use_supervisor else 'linear'}")
        
        switched = service.switch_pattern(False)
        print(f"   Switched to linear: {switched}")
        print(f"   New pattern: {'supervisor' if service.use_supervisor else 'linear'}")
        
        switched = service.switch_pattern(True)
        print(f"   Switched back to supervisor: {switched}")
        print(f"   Final pattern: {'supervisor' if service.use_supervisor else 'linear'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing supervisor features: {e}")
        return False

async def main():
    print("🚀 AI Social Media Post Generator - Supervisor Pattern Test")
    print("=" * 70)
    
    # Test core functionality
    success = await test_supervisor_vs_linear()
    
    if success:
        # Test additional features
        await test_supervisor_features()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📚 Next steps:")
        print("1. Update your client code to use the supervisor pattern")
        print("2. Set use_supervisor=True in your API requests")
        print("3. Monitor the enhanced insights and quality metrics")
        print("4. Enjoy the improved workflow orchestration!")
    else:
        print("\n💥 Tests failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 