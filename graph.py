"""
This script generates a Mermaid dependency graph for a Jira epic.

Usage:
python graph.py <epic_key> [--blocks-linktype <link_type>] [--closed-status <status>] [--skip-closed]
"""


import argparse
import os
from jira import JIRA
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate a Mermaid dependency graph for a Jira epic')
parser.add_argument('epic_key', help='The key of the epic to analyze (e.g. DATA-3377)')
parser.add_argument('--blocks-linktype', default='Blocks',
    help='The Jira link type to follow (default: Blocks)')
parser.add_argument('--closed-status', default='closed',
    help='The status name that indicates a closed issue (default: closed)')
parser.add_argument('--skip-closed', action='store_true',
    help='Skip closed issues in the graph')
args = parser.parse_args()

# Get credentials from environment variables
jira_email = os.getenv('JIRA_EMAIL')
jira_token = os.getenv('JIRA_API_TOKEN')
jira_url = os.getenv('JIRA_URL')

if not jira_email or not jira_token or not jira_url:
    raise ValueError("Please set JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_URL environment variables")

# Authenticate
jira = JIRA(
    server=jira_url,
    basic_auth=(jira_email, jira_token)
)

# Get all child issues in the epic
epic_key = args.epic_key
issues = jira.search_issues(f'"Epic Link" = {epic_key}', maxResults=500)

nodes = {}
edges = []

# Collect nodes and dependency edges
for issue in issues:
    key = issue.key
    summary = issue.fields.summary.replace('"', '\\"')
    status = issue.fields.status.name.lower()
    if args.skip_closed and status == args.closed_status:
        continue
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
        print(f'    style {key} fill:#eee,stroke:#999,text-decoration:line-through')

# Add final epic node
print(f'    {epic_key}["<a href="{jira_url}/browse/{epic_key}">{epic_key}</a><br>Epic"]')
print(f'    style {epic_key} fill:#e6f3ff,stroke:#4d9fff,stroke-width:2px')

# Render dependencies
for src, dst in edges:
    print(f"    {src} --> {dst}")

# Connect leaf nodes to epic
for leaf in leaf_nodes:
    print(f"    {leaf} --> {epic_key}")
