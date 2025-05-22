from jira import JIRA
import argparse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate a Mermaid dependency graph for a Jira epic')
parser.add_argument('epic_key', help='The key of the epic to analyze (e.g. DATA-3377)')
parser.add_argument('--blocks-linktype', default='Blocks', help='The Jira link type to follow (default: Blocks)')
parser.add_argument('--closed-status', default='closed', help='The status name that indicates a closed issue (default: closed)')
args = parser.parse_args()

# Get credentials from environment variables
jira_email = os.getenv('JIRA_EMAIL')
jira_token = os.getenv('JIRA_API_TOKEN')
jira_url = os.getenv('JIRA_URL')

if not jira_email or not jira_token or not jira_url:
    raise ValueError("Please set JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_URL environment variables in .env file")

# Authenticate
jira = JIRA(
    server=jira_url,
    basic_auth=(jira_email, jira_token)
)

# Get all child issues in the epic
jql = f'"Epic Link" = {args.epic_key}'
issues = jira.search_issues(jql, maxResults=500)

nodes = {}
edges = []

# Collect nodes and dependency edges
for issue in issues:
    key = issue.key
    summary = issue.fields.summary.replace('"', '\\"')
    status = issue.fields.status.name.lower()
    nodes[key] = (summary, status)

    for link in issue.fields.issuelinks:
        if hasattr(link, "outwardIssue") and link.type.name == args.blocks_linktype:
            target = link.outwardIssue.key
            if target in nodes:
                edges.append((key, target))
        elif hasattr(link, "inwardIssue") and link.type.name == args.blocks_linktype:
            source = link.inwardIssue.key
            if source in nodes:
                edges.append((source, key))

# Find leaf nodes (nodes that aren't blocking any other issues)
blocking_nodes = {src for src, _ in edges}
leaf_nodes = set(nodes.keys()) - blocking_nodes

# Create Mermaid output
print("---")
print("config:")
print("  layout: elk")
print("---")
print("flowchart TD")
for key, (summary, status) in nodes.items():
    print(f'    {key}["<a href="{jira_url}/browse/{key}">{key}</a><br>{summary}"]')
    if status == args.closed_status:
        print(f'    style {key} fill:#f0f0f0,stroke:#999,stroke-width:1px,text-decoration:line-through')

# Add final epic node
print(f'    {args.epic_key}["<a href="{jira_url}/browse/{args.epic_key}">{args.epic_key}</a><br>Epic"]')
print(f'    style {args.epic_key} fill:#e6f3ff,stroke:#4d9fff,stroke-width:2px')

# Render dependencies
for src, dst in edges:
    print(f"    {src} --> {dst}")

# Connect leaf nodes to epic
for leaf in leaf_nodes:
    print(f"    {leaf} --> {args.epic_key}")
