---
name: content
description: |
  Main entry point for the 10X Content Expert system. Routes content creation requests
  to appropriate skills and agents. Use /content to access all content creation capabilities.
---

# /content Command

The main entry point for the 10X Content Expert system.

## Usage

```
/content [action] [options]
```

## Available Actions

### Content Creation

| Command | Description | Routes To |
|---------|-------------|-----------|
| `/content email` | Create email copy | email-copywriter |
| `/content social` | Create social media content | social-media-writer |
| `/content ppt` | Create presentation content | presentation-content |
| `/content blog` | Create blog/article content | blog-article-writer |
| `/content hooks` | Generate headlines, hooks, CTAs | hook-generator |
| `/content sequence` | Create email nurture sequence | nurture-sequence |
| `/content repurpose` | Transform content across formats | content-repurposer |

### Analysis & Planning

| Command | Description | Routes To |
|---------|-------------|-----------|
| `/content analyze` | Analyze references and transcripts | content-analyzer |
| `/content plan` | Create a content plan | content-planner agent |
| `/content voice` | Manage brand voice | brand-voice-manager |
| `/content frameworks` | Reference copywriting frameworks | content-frameworks |

### Workflow

| Command | Description | Routes To |
|---------|-------------|-----------|
| `/content project` | Start a full content project | content-manager |
| `/content create` | Execute an approved plan | content-executor agent |

### Media & Cloud

| Command | Description | Routes To |
|---------|-------------|-----------|
| `/content transcribe` | Transcribe audio/video locally | mega-transcriber |
| `/content mega` | Browse/download MEGA cloud files | mega-manager |
| `/content canvas` | Create interactive visual canvas | tldraw-canvas |

### Local File Operations

| Command | Description | Routes To |
|---------|-------------|-----------|
| `/content edit` | Edit local files | local-file-manager |
| `/content pptx` | Edit PowerPoint files | local-pptx-editor |
| `/content docx` | Edit Word documents | local-docx-editor |
| `/content pdf` | Edit PDF files | local-pdf-editor |
| `/content xlsx` | Edit Excel files | local-xlsx-editor |

## Quick Start Examples

### Create Social Media Content
```
/content social
> "Write LinkedIn posts about productivity tips"
```

### Create Email Sequence
```
/content sequence
> "Create a 5-email welcome sequence for new subscribers"
```

### Analyze Transcripts
```
/content analyze
> "Analyze my training transcripts for content ideas"
```

### Full Content Project
```
/content project
> "I need content for my product launch - emails, social, and presentation"
```

## Workflow Guide

### For Quick Content

1. Use specific commands: `/content email`, `/content social`, etc.
2. Describe what you need
3. Answer clarifying questions
4. Get your content

### For Content Projects

1. Start with `/content analyze` to understand your references
2. Use `/content plan` to create a strategic plan
3. Get plan approval
4. Use `/content create` to execute the plan

### For Repurposing

1. Use `/content repurpose`
2. Point to source content (transcript, blog, etc.)
3. Specify desired output formats
4. Get multi-platform content

## Reference Materials

The system learns from your reference materials in:

```
references/
├── transcripts/     # Video/audio transcripts
├── examples/        # High-performing content examples
├── brand-voice/     # Brand guidelines
└── templates/       # Content templates
```

Add your materials to these folders for better, more personalized content.

## Output Location

All generated content is saved to:

```
output/
├── content/         # Generated content
│   ├── emails/
│   ├── social/
│   ├── presentations/
│   └── blogs/
├── analysis/        # Analysis results
└── plans/           # Content plans
```

## Tips

1. **Start with references** - Add your transcripts and examples for better results
2. **Define brand voice** - Use `/content voice` to ensure consistency
3. **Use the planner** - For big projects, start with `/content plan`
4. **Iterate** - Request revisions and variations as needed

## Need Help?

- `/content` - Shows this help
- Ask "What content can you create?" for capabilities overview
- Ask "How do I [specific task]?" for guidance
