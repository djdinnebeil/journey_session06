#!/usr/bin/env python3
"""
Simple integration test for the AI Social Media Post Generator
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, '.')

async def test_post_generation():
    """Test the post generation workflow"""
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
        
        # Import and test the service
        from api.services.post_generator import PostGeneratorService
        
        print("🧪 Testing post generation service...")
        service = PostGeneratorService()
        
        # Test with a sample paper title
        test_title = "LoRA: Low-Rank Adaptation of Large Language Models"
        print(f"📝 Generating post for: {test_title}")
        
        result = await service.generate_post(test_title)
        
        print("\n✅ Post generation successful!")
        print(f"📄 Summary length: {len(result['summary'])} characters")
        print(f"📱 Post length: {len(result['post'])} characters")
        print(f"✅ Technical check: {result['tech_check']}")
        print(f"🎨 Style check: {result['style_check']}")
        print(f"🔁 Revisions: {result['revision_count']}")
        print(f"✔️ Final result: {result['verify_result']}")
        
        # Display the generated post
        print(f"\n📝 Generated Post:\n{'-'*50}")
        print(result['post'])
        print('-'*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 AI Social Media Post Generator - Integration Test")
    print("="*60)
    
    success = await test_post_generation()
    
    if success:
        print("\n🎉 All tests passed! The application is ready to deploy.")
        print("\nNext steps:")
        print("1. Run 'npm install' to install frontend dependencies")
        print("2. Run 'npm run dev' to start the frontend")
        print("3. Run 'python -m uvicorn api.main:app --reload' to start the backend")
        print("4. Or deploy to Vercel with 'vercel deploy'")
    else:
        print("\n💥 Tests failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 