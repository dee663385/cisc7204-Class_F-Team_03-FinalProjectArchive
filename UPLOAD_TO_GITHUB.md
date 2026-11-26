# Upload to GitHub

The current project folder is not a Git repository and no public remote URL was supplied. Use the steps below after creating an empty public repository.

Suggested repository name:

`cisc7204-Class_F-Team_03-FinalProjectArchive`

## Command-line method

```powershell
cd cisc7204-Class_F-Team_03-FinalProjectArchive
git init
git add .
git commit -m "Final project archive"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/cisc7204-Class_F-Team_03-FinalProjectArchive.git
git push -u origin main
```

Then replace the placeholder URL in `README.md`, commit, and push again.

## Browser method

1. Create a new public GitHub repository with the suggested name.
2. Use **Add file > Upload files**.
3. Upload the contents of this folder while preserving the directory structure.
4. Commit the upload.
5. Copy the repository URL into `README.md`.
6. Open the repository in a private browser window and confirm that it is publicly accessible.
