# Windows PowerShell
mkdir eco-watt-ai-submission
cd eco-watt-ai-submission
git init
git add .
git commit -m "Initial Eco-Watt AI project"
Compress-Archive -Path * -DestinationPath eco-watt-ai-submission.zip

# macOS/Linux
mkdir eco-watt-ai-submission
cd eco-watt-ai-submission
git init
git add .
git commit -m "Initial Eco-Watt AI project"
zip -r eco-watt-ai-submission.zip .
