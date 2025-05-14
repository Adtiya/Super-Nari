
#!/bin/bash

echo "🚀 Starting Super NARI Backend..."
gnome-terminal -- bash -c "cd main && uvicorn main:app --reload; exec bash"

sleep 5

echo "💻 Starting Super NARI Flutter Frontend..."
gnome-terminal -- bash -c "cd nari_flutter_dashboard && flutter run -d chrome; exec bash"

echo "✅ Both backend and frontend launched"
