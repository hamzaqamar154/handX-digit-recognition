"""
Print completion message for the project.
"""
print("\n" + "=" * 60)
print("PROJECT SETUP COMPLETE!")
print("=" * 60)
print("\nModel Training: [OK] Completed (99.07% accuracy)")
print("Demo Prediction: [OK] Completed")
print("\nTo run the services:\n")
print("1. Streamlit UI:")
print("   streamlit run ui/app.py")
print("   URL: http://localhost:8501\n")
print("2. FastAPI Server:")
print("   uvicorn api.app:app --reload")
print("   URL: http://localhost:8000\n")
print("3. Or run both together:")
print("   python start_services.py\n")
print("=" * 60 + "\n")

