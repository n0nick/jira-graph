# Jira Epic Dependency Graph Generator

This script generates a [Mermaid](https://mermaid.js.org/) flowchart showing the dependency
relationships between issues in a Jira epic.  It's particularly useful for visualizing the structure
and progress of complex epics.

## Setup

1. Get your Jira API token:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Give it a name and copy the token value

2. Create a `.env` file in the project directory with your Jira credentials:
```bash
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your-api-token
JIRA_URL=https://your-company.atlassian.net
```

## Usage

Install dependencies:
```bash
pip install -r requirements.txt
```

Basic usage:
```bash
python graph.py EPIC-KEY
```

Example:
```bash
python graph.py DATA-3377
```

### Command Line Options

- `EPIC-KEY`: The key of the epic to analyze (required)
- `--skip-closed`: Skip rendering closed issues in the graph
- `--blocks-linktype`: The Jira link type to follow (default: "Blocks")
- `--closed-status`: The status name that indicates a closed issue (default: "closed")

Examples:
```bash
# Use a different link type
python graph.py DATA-3377 --blocks-linktype "Relates to"

# Use a different closed status
python graph.py DATA-3377 --closed-status "done"
```

## Output

The script outputs a Mermaid flowchart that can be rendered in:
- GitHub markdown
- Mermaid Live Editor (https://mermaid.live)
- VS Code with Mermaid extension
- Other Mermaid-compatible tools

The flowchart includes:
- All issues in the epic
- Dependencies between issues
- Links to Jira for each issue
- Visual distinction for closed issues
- Connection of leaf nodes to the epic

## Example Output

```mermaid
---
config:
  layout: elk
---
flowchart TD
    DOCS-1001["<a href='https://example.atlassian.net/browse/DOCS-1001'>DOCS-1001</a><br>Document feature implementation"]
    DATA-1002["<a href='https://example.atlassian.net/browse/DATA-1002'>DATA-1002</a><br>Implement core feature"]
    DATA-1003["<a href='https://example.atlassian.net/browse/DATA-1003'>DATA-1003</a><br>Setup infrastructure"]
    style DATA-1003 fill:#eee,stroke:#999,text-decoration:line-through
    DATA-1004["<a href='https://example.atlassian.net/browse/DATA-1004'>DATA-1004</a><br>Add metadata support"]
    style DATA-1004 fill:#eee,stroke:#999,text-decoration:line-through
    DATA-1005["<a href='https://example.atlassian.net/browse/DATA-1005'>DATA-1005</a><br>Implement data processing"]
    DATA-1006["<a href='https://example.atlassian.net/browse/DATA-1006'>DATA-1006</a><br>Setup data pipeline"]
    DATA-1007["<a href='https://example.atlassian.net/browse/DATA-1007'>DATA-1007</a><br>Add UI components"]
    style DATA-1007 fill:#eee,stroke:#999,text-decoration:line-through
    DATA-1008["<a href='https://example.atlassian.net/browse/DATA-1008'>DATA-1008</a><br>Implement API endpoints"]
    DATA-1009["<a href='https://example.atlassian.net/browse/DATA-1009'>DATA-1009</a><br>Add authentication"]
    style DATA-1009 fill:#eee,stroke:#999,text-decoration:line-through
    DATA-1010["<a href='https://example.atlassian.net/browse/DATA-1010'>DATA-1010</a><br>Setup monitoring"]
    DATA-1011["<a href='https://example.atlassian.net/browse/DATA-1011'>DATA-1011</a><br>Epic"]
    style DATA-1011 fill:#e6f3ff,stroke:#4d9fff,stroke-width:2px
    DATA-1004 --> DATA-1005
    DATA-1006 --> DATA-1005
    DATA-1003 --> DATA-1008
    DATA-1007 --> DATA-1008
    DATA-1009 --> DATA-1008
    DATA-1005 --> DATA-1002
    DATA-1008 --> DATA-1002
    DATA-1010 --> DATA-1002
    DATA-1002 --> DATA-1011
    DOCS-1001 --> DATA-1011
```

Tip: You can render the Mermaid output in [mermaid.live](https://mermaid.live/) or as a GitHub Gist:
https://gist.github.com/n0nick/bdf92b57c510fd3eaa498a22dbb2637b