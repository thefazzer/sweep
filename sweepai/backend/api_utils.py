def get_pr_snippets(
    repo_name: str,
    annotations: dict,
    cloned_repo: MockClonedRepo,
):
    pr_snippets = []
    skipped_pr_snippets = []
    sweep_config = SweepConfig()
    pulls = annotations.get("pulls", [])
    pulls_messages = ""
    for pull in pulls:
        patch = pull["file_diffs"]
        diff_patch = ""
        # Filters copied from get_pr_changes
        for file_data in patch:
            file_path = file_data["filename"]
            if sweep_config.is_file_excluded(file_path):
                continue
            try:
                file_contents = cloned_repo.get_file_contents(file_path)
            except FileNotFoundError:
                logger.warning(f"Error getting file contents for {file_path}")
                continue
            is_file_suitable, reason = sweep_config.is_file_suitable(file_contents)
            if not is_file_suitable:
                continue
            diff = file_data["patch"]
            # Add null check here
            if diff is None:
                logger.warning(f"No diff found for {file_path}")
                continue
            if file_data["status"] == "added":
                pr_snippets.append(Snippet.from_file(file_path, file_contents))
            elif file_data["status"] == "modified":
                patches = split_diff_into_patches(diff, file_path)
                num_changes_per_patch = [
                    patch.changes.count("\n+") + patch.changes.count("\n-")
                    for patch in patches
                ]
                if (
                    max(num_changes_per_patch) > 10
                    or file_contents.count("\n") + 1 < 10 * file_data["changes"]
                ):
                    pr_snippets.append(Snippet.from_file(file_path, file_contents))
                else:
                    skipped_pr_snippets.append(
                        Snippet.from_file(file_path, file_contents)
                    )
            if file_data["status"] in ("added", "modified", "removed"):
                diff_patch += (
                    f"File: {file_path}\n"
                    + remove_whitespace_changes(diff).strip("\n")
                    + "\n\n"
                )
        if diff_patch:
            pulls_messages += (
                pr_format.format(
                    url=f"https://github.com/{repo_name}/pull/{pull['number']}",
                    title=pull["title"],
                    body=pull["body"],
                    patch=diff_patch.strip("\n"),
                )
                + "\n\n"
            )
    return pr_snippets, skipped_pr_snippets, pulls_messages


from loguru import logger
from sweepai.config.client import SweepConfig
from sweepai.core.entities import Snippet
from sweepai.utils.diff import remove_whitespace_changes
from sweepai.utils.github_utils import MockClonedRepo
from sweepai.core.review_utils import split_diff_into_patches
