from github import Github

class GitHubClient:
    def __init__(self, api_token, repo_owner, repo_name):
        self.github = Github(api_token)
        self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")

    def create_or_update_file(self, file_path, content, commit_message):
        try:
            contents = self.repo.get_contents(file_path)
            self.repo.update_file(contents.path, commit_message, content, contents.sha)
        except:
            self.repo.create_file(file_path, commit_message, content)

    def get_open_pull_requests(self):
        return self.repo.get_pulls(state='open')

    def comment_on_pull_request(self, pr_number, comment):
        pr = self.repo.get_pull(pr_number)
        pr.create_issue_comment(comment)

    def suggest_changes(self, pr_number, suggestions):
        pr = self.repo.get_pull(pr_number)
        for file_path, suggestion in suggestions.items():
            pr.create_review_comment(body=suggestion, commit_id=pr.head.sha, path=file_path, line=1)