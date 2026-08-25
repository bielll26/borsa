#!/usr/bin/env python3
"""
Create comprehensive PDF for Ad Creators Lab course analysis.
Includes all frameworks, strategies, explanations, and reasoning.
"""

import os
import sys
from datetime import datetime

# Set encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Output path
OUTPUT_PATH = r"C:\Users\Anit\Downloads\10x-Content-Expert\output\pdf"
os.makedirs(OUTPUT_PATH, exist_ok=True)

def create_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()

    # Title style
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a365d')
    ))

    # Subtitle
    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#4a5568')
    ))

    # Section Header
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=20,
        spaceBefore=25,
        spaceAfter=15,
        textColor=colors.HexColor('#2c5282'),
        borderPadding=10
    ))

    # Subsection Header
    styles.add(ParagraphStyle(
        name='SubsectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#2b6cb0')
    ))

    # Framework Title
    styles.add(ParagraphStyle(
        name='FrameworkTitle',
        parent=styles['Heading3'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
        textColor=colors.HexColor('#3182ce'),
        fontName='Helvetica-Bold'
    ))

    # Body text
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=16
    ))

    # Bullet point
    styles.add(ParagraphStyle(
        name='BulletText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        leftIndent=20,
        leading=14
    ))

    # Example text
    styles.add(ParagraphStyle(
        name='ExampleText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        leftIndent=30,
        textColor=colors.HexColor('#4a5568'),
        fontName='Helvetica-Oblique',
        leading=14
    ))

    # Highlight box
    styles.add(ParagraphStyle(
        name='HighlightText',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        backColor=colors.HexColor('#ebf8ff'),
        borderPadding=8,
        leading=16
    ))

    # Reason/Why text
    styles.add(ParagraphStyle(
        name='ReasonText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        leftIndent=15,
        textColor=colors.HexColor('#2d3748'),
        backColor=colors.HexColor('#f7fafc'),
        borderPadding=6,
        leading=14
    ))

    return styles

def add_section_divider(story):
    """Add a visual divider between sections."""
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor('#e2e8f0')))
    story.append(Spacer(1, 10))

def build_pdf():
    """Build the complete PDF document."""

    filename = os.path.join(OUTPUT_PATH, f"2026-01-31_Ad_Creators_Lab_Complete_Guide.pdf")
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = create_styles()
    story = []

    # ==================== TITLE PAGE ====================
    story.append(Spacer(1, 100))
    story.append(Paragraph("AD CREATORS LAB", styles['MainTitle']))
    story.append(Paragraph("Complete Framework Guide", styles['Subtitle']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("AI Ads That Scale", styles['Subtitle']))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Comprehensive Analysis for Ecommerce Managers", styles['CustomBody']))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['CustomBody']))
    story.append(Spacer(1, 30))

    # Table of Contents
    toc_data = [
        ["Section", "Page"],
        ["1. Executive Summary", "3"],
        ["2. Campaign Frameworks (12 Types)", "4"],
        ["3. Brand Messaging Guidelines", "20"],
        ["4. Audience Targeting Strategies", "24"],
        ["5. Implementation Strategies", "28"],
        ["6. Campaign Planning & Structure", "32"],
        ["7. Framework Quick Reference", "36"],
        ["8. Complete Framework Scripts", "38"],
    ]

    toc_table = Table(toc_data, colWidths=[4*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ==================== EXECUTIVE SUMMARY ====================
    story.append(Paragraph("1. EXECUTIVE SUMMARY", styles['SectionHeader']))

    story.append(Paragraph(
        "This comprehensive guide extracts and organizes all key frameworks, strategies, and methodologies "
        "from the Ad Creators Lab course. It is designed specifically for ecommerce managers who need to "
        "create high-converting ad campaigns that scale.",
        styles['CustomBody']
    ))

    story.append(Paragraph("What This Guide Contains:", styles['SubsectionHeader']))

    summary_points = [
        "<b>12 Proven Ad Frameworks</b> - Complete scripts, explanations, and use cases for each framework",
        "<b>Brand Messaging Guidelines</b> - Hook formulas, voice guidelines, and messaging structures",
        "<b>Audience Targeting Strategies</b> - How to segment and target different buyer types",
        "<b>Implementation Strategies</b> - Research protocols, testing methods, and optimization tactics",
        "<b>Campaign Planning Templates</b> - Ready-to-use briefs, calendars, and checklists"
    ]

    for point in summary_points:
        story.append(Paragraph(f"- {point}", styles['BulletText']))

    story.append(Spacer(1, 15))
    story.append(Paragraph("Key Insight from the Course:", styles['SubsectionHeader']))
    story.append(Paragraph(
        "<b>WHY THIS MATTERS:</b> The Ad Creators Lab emphasizes that successful ads are not about "
        "copying what's 'longest running' - those are often lowest-funnel retargeting ads. Instead, "
        "success comes from understanding your audience's market awareness level, using proven "
        "psychological frameworks, and testing multiple hook variations systematically.",
        styles['ReasonText']
    ))

    story.append(PageBreak())

    # ==================== SECTION 2: CAMPAIGN FRAMEWORKS ====================
    story.append(Paragraph("2. CAMPAIGN FRAMEWORKS", styles['SectionHeader']))

    story.append(Paragraph(
        "The Ad Creators Lab teaches 12 distinct advertising frameworks, each designed for specific "
        "situations and audience types. Below is a complete breakdown of each framework with explanations "
        "of WHY each element works psychologically.",
        styles['CustomBody']
    ))

    # ---------- FRAMEWORK 1: BANDWAGON EFFECT ----------
    story.append(Paragraph("2.1 Bandwagon Effect - CROWD Framework", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework leverages social proof and the psychological tendency for people "
        "to follow what experts, authorities, or large groups are doing. It positions your product as part "
        "of a movement that smart people are joining.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Products with expert endorsements, trending products, health/wellness, "
        "any product where authority figures or experts can be referenced.", styles['CustomBody']))

    story.append(Paragraph("The CROWD Framework Structure:", styles['FrameworkTitle']))

    crowd_elements = [
        ("<b>C - Call out the movement:</b>",
         "Create curiosity by calling out what relevant groups of people, experts, or authority figures are doing.",
         "WHY IT WORKS: Triggers FOMO and social proof. People trust what experts do more than what brands say.",
         "Example: 'Why do anti-aging experts swear by copper peptides over collagen?'"),

        ("<b>R - Reject the old way:</b>",
         "Educate the viewer on why the common solution isn't as effective as they think.",
         "WHY IT WORKS: Creates cognitive dissonance. Makes them question their current approach and opens them to alternatives.",
         "Example: 'Most people spend thousands on anti-aging creams, but your body already makes a natural compound...'"),

        ("<b>O - Onboard the new way:</b>",
         "Introduce your product/service as the superior solution.",
         "WHY IT WORKS: After rejecting the old, the viewer needs a new solution. You fill that gap immediately.",
         "Example: 'Soothe Supps puts this powerful compound into a peptide that works at a cellular level.'"),

        ("<b>W - Wave the proof:</b>",
         "Build trust by showing social proof, studies, case studies, etc.",
         "WHY IT WORKS: Reduces skepticism with evidence. Multiple proof types compound trust.",
         "Example: 'This isn't just another \"special ingredient\" - it's backed by clinical studies and results.'"),

        ("<b>D - Direct the viewer:</b>",
         "Get viewers to check out your product/service with a clear CTA.",
         "WHY IT WORKS: After building desire and trust, you need to channel that energy into action.",
         "Example: 'Get it at Soothe Supps right now to look and feel younger.'")
    ]

    for element, desc, reason, example in crowd_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    add_section_divider(story)

    # ---------- FRAMEWORK 2: INDUSTRY CONTRARIAN ----------
    story.append(Paragraph("2.2 Industry Contrarian - DISRUPT Framework", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework positions your brand as a truth-teller exposing industry secrets "
        "or failures. It builds trust by being the one to 'lift the curtain' on what others won't say.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Products that challenge industry norms, disruptive solutions, "
        "brands that can back claims with strong evidence.", styles['CustomBody']))

    story.append(Paragraph("The DISRUPT Framework Structure:", styles['FrameworkTitle']))

    disrupt_elements = [
        ("<b>D - Declassify the secret:</b>",
         "Expose suppressed industry knowledge or debunk myths.",
         "WHY IT WORKS: Creates instant intrigue. People love feeling like they're getting 'insider' information.",
         "Example: 'Scientists discovered this anti-aging compound in 1973, but the beauty industry kept it quiet.'"),

        ("<b>I - Industry failure:</b>",
         "Explain why mainstream solutions fail.",
         "WHY IT WORKS: Validates frustrations the viewer already has. Creates an 'enemy' to rally against.",
         "Example: 'Let's be honest, most anti-aging products are just expensive moisturizers.'"),

        ("<b>S - Solution:</b>",
         "Introduce your product as the answer.",
         "WHY IT WORKS: After exposing the problem, you present the logical solution.",
         "Example: 'But GHK-Cu is different. This copper peptide tells your skin cells to act younger at a DNA level.'"),

        ("<b>R - Reinforce with evidence:</b>",
         "Validate with studies, scientific discoveries, real-life examples.",
         "WHY IT WORKS: Transforms claims into facts. Evidence is harder to argue against.",
         "Example: '300+ studies have proven it stimulates collagen, reduces inflammation, and accelerates skin repair.'"),

        ("<b>U - Upstage the competition:</b>",
         "Show what makes your solution unique.",
         "WHY IT WORKS: Differentiates you from alternatives. Gives a reason to choose YOU specifically.",
         "Example: 'You don't need injections - Soothe Supps offers GHK-Cu capsules.'"),

        ("<b>P - Provide proof:</b>",
         "Show measurable real-world adoption (social proof).",
         "WHY IT WORKS: Removes the 'am I the only one?' fear. Shows others have already validated the choice.",
         "Example: 'People are seeing visibly firmer skin, thicker hair, and reduced fine lines in weeks.'"),

        ("<b>T - Trigger the movement:</b>",
         "CTA with risk reversal or urgency.",
         "WHY IT WORKS: Removes final objection (risk) and creates momentum to act now.",
         "Example: 'Try risk-free for 30 nights - track your improvement or get a full refund.'")
    ]

    for element, desc, reason, example in disrupt_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    add_section_divider(story)
    story.append(PageBreak())

    # ---------- FRAMEWORK 3: LISTICLE ----------
    story.append(Paragraph("2.3 Listicle - CURE Framework", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework uses numbered lists to create curiosity and structure. "
        "Lists are inherently engaging because they promise organized, digestible information.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Problem-solution products, educational content, comparison ads, "
        "products that solve multiple pain points.", styles['CustomBody']))

    story.append(Paragraph("The CURE Framework Structure:", styles['FrameworkTitle']))

    cure_elements = [
        ("<b>C - Curiosity (List Hook):</b>",
         "Spark intrigue with a numbered hook.",
         "WHY IT WORKS: Numbers create specificity and promise. '5 mistakes' is more compelling than 'mistakes' because it sets an expectation.",
         "Example: 'Top 3 reasons your cellulite isn't going away'"),

        ("<b>U - Uncover failures:</b>",
         "Expose why standard approaches fail (list each one).",
         "WHY IT WORKS: Each failure point validates the viewer's past struggles. They think 'Yes! I've tried that and it didn't work!'",
         "Example: '1. Anti-aging creams that only touch the surface. 2. Expensive laser treatments that aren't permanent. 3. Miracle ingredients with no clinical proof.'"),

        ("<b>R - Remedy:</b>",
         "Introduce your product as the answer.",
         "WHY IT WORKS: After listing failures, you present the ONE solution that actually works.",
         "Example: 'So what actually works? SOD B Dimpless - the only ingredient clinically proven to reduce cellulite.'"),

        ("<b>E - Evidence:</b>",
         "Add credibility through social proof and data.",
         "WHY IT WORKS: Proof turns claims into facts. Specific numbers are more believable.",
         "Example: 'Thousands of women are seeing smoother thighs and renewed confidence after just 12 weeks.'"),

        ("<b>E - Engage (CTA):</b>",
         "Drive action with risk reversal.",
         "WHY IT WORKS: Removes the final barrier - the fear of wasting money.",
         "Example: 'Try it risk-free for 60 days and see the difference yourself.'")
    ]

    for element, desc, reason, example in cure_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    add_section_divider(story)

    # ---------- FRAMEWORK 4: FOUNDER ----------
    story.append(Paragraph("2.4 Founder-Led - FOUNDER Framework", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework puts a human face on the brand by featuring the founder's story. "
        "It creates emotional connection through personal narrative and shared mission.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Brand storytelling, mission-driven brands, startups, "
        "products where authenticity and origin story matter.", styles['CustomBody']))

    story.append(Paragraph("The FOUNDER Framework Structure:", styles['FrameworkTitle']))

    founder_elements = [
        ("<b>F - Feature the founder:</b>",
         "Introduce founder(s) as relatable humans behind a great mission.",
         "WHY IT WORKS: People buy from people, not companies. A real person creates trust and relatability.",
         "Example: 'This is Mike and he's a regular guy. This is Nick... and he's sleeping right now.'"),

        ("<b>O - Opposing force:</b>",
         "Present the enemy/problem that your ideal buyer faces.",
         "WHY IT WORKS: Creating a common enemy unites you with the viewer. You're on the same side.",
         "Example: 'In South Africa, we've got more private security officers than police. Over 30 million people are using WhatsApp groups for safety, but it's a mess.'"),

        ("<b>U - Unlocking the idea:</b>",
         "Reveal the breakthrough moment. Frame your solution as an intuitive pivot.",
         "WHY IT WORKS: The 'eureka moment' creates narrative tension and resolution. It's satisfying to watch.",
         "Example: 'So we thought - what if we could take all these WhatsApp groups and turn them into something actually useful?'"),

        ("<b>N - Numbers:</b>",
         "Present 3-4 tangible desired outcomes (numbers, timelines, revenue).",
         "WHY IT WORKS: Specific numbers create credibility. Vague claims are forgettable; specific ones stick.",
         "Example: 'In just 4 months: Mapped over 500 crimes, helped 2,000 people get home safely, got 6 major security companies using our system.'"),

        ("<b>D - Destiny:</b>",
         "Position current wins as just the beginning of a larger mission.",
         "WHY IT WORKS: Shows ambition and longevity. Viewers want to back winners with big visions.",
         "Example: 'We're just getting started. Brazil, Mexico, Colombia - they all have the same problem. And we've got the solution.'"),

        ("<b>E - Engage the movement:</b>",
         "CTA framing supporters as co-revolutionaries.",
         "WHY IT WORKS: Elevates the action from 'buying' to 'joining a cause'. Creates identity and belonging.",
         "Example: 'So comment Wolf to help prevent crime. Join the movement.'")
    ]

    for element, desc, reason, example in founder_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    add_section_divider(story)
    story.append(PageBreak())

    # ---------- FRAMEWORK 5: SIMPLE ----------
    story.append(Paragraph("2.5 How You Can X Without Y - SIMPLE Framework", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework addresses the desire for results without the usual hassle. "
        "It positions your product as the shortcut that eliminates friction.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Convenience products, time-saving solutions, busy professionals, "
        "products that simplify complex routines.", styles['CustomBody']))

    story.append(Paragraph("The SIMPLE Framework Structure:", styles['FrameworkTitle']))

    simple_elements = [
        ("<b>S - State the escape:</b>",
         "Address identity + pain in one line.",
         "WHY IT WORKS: Immediately qualifies the viewer and speaks to their specific situation.",
         "Example: 'If you're a busy dad and hate skincare routines, this is for you.'"),

        ("<b>I - Identify pain:</b>",
         "Mirror frustrations with specific scenarios they face.",
         "WHY IT WORKS: Specificity creates recognition. Generic pain points feel like marketing; specific ones feel like understanding.",
         "Example: 'As a dad, life moves fast. Between work, family, and everything in between, I rarely have time for complicated skin routines.'"),

        ("<b>M - Minimal solution:</b>",
         "Introduce your product as the 'one-thing fix'.",
         "WHY IT WORKS: Overwhelmed people want simplicity. 'The only thing you need' is incredibly appealing.",
         "Example: 'Which is why I started using this all-natural balm. I put it on my face in the morning, and it locks in hydration for the whole day.'"),

        ("<b>P - Prove:</b>",
         "Connect ingredients/features to tangible benefits using 'because so' logic.",
         "WHY IT WORKS: Features alone don't sell; benefits do. Linking them creates understanding.",
         "Example: 'The beeswax protects my skin from harsh weather without feeling greasy. The raw honey soothes irritation.'"),

        ("<b>L - Lifestyle win:</b>",
         "Contrast past effort with desired outcome.",
         "WHY IT WORKS: Before/after contrast makes the value tangible and visual.",
         "Example: 'I love this because there's no fancy steps - you just apply it and boom, you're done.'"),

        ("<b>E - Escape CTA:</b>",
         "Urge action with identity-tailored language.",
         "WHY IT WORKS: Speaking to their identity makes it personal. It's not a generic ad; it's FOR them.",
         "Example: 'So if you're a dad tired of dry skin but don't want to add a whole chore to your day, grab this tallow balm now.'")
    ]

    for element, desc, reason, example in simple_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    add_section_divider(story)

    # ---------- FRAMEWORK 6: PURE ----------
    story.append(Paragraph("2.6 Organic/Authentic - PURE Framework", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework embraces raw, unpolished authenticity. It shows your product "
        "in real-life situations with genuine reactions rather than scripted testimonials.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Products with real-world testing, durability claims, lifestyle products, "
        "brands that value authenticity over polish.", styles['CustomBody']))

    story.append(Paragraph("The PURE Framework Structure:", styles['FrameworkTitle']))

    pure_elements = [
        ("<b>P - Problem uncovered:</b>",
         "Hook with raw, relatable frustration using blunt language.",
         "WHY IT WORKS: Bluntness cuts through the noise. It feels real, not marketing-speak.",
         "Example: 'Every mascara I've ever tried ends up looking like sh*t by the end of the day. Except this one.'"),

        ("<b>U - Unfiltered chaos:</b>",
         "Show benefits in everyday life scenarios (2-3 real situations).",
         "WHY IT WORKS: Real scenarios create mental movies. Viewers imagine themselves in those situations.",
         "Example: 'At 7am I applied mascara. By 10am - 3 sweaty meetings. By 4pm - coffee crisis. By 7:45pm I got home exhausted. But my lashes were still perfect.'"),

        ("<b>R - Real evidence:</b>",
         "Prove performance through organic discovery moments.",
         "WHY IT WORKS: Genuine 'aha moments' are more believable than claims. It feels like discovery, not selling.",
         "Example: 'Now I thought it was gonna be hard to remove but this tubing mascara literally slides off with warm water.'"),

        ("<b>E - Effortless freedom:</b>",
         "Reveal the anti-hassle payoff contrasting easy solution against past struggles.",
         "WHY IT WORKS: The payoff - ease and freedom - is the ultimate benefit people crave.",
         "Example: 'Which just makes this mascara that much better, especially after a long day.'")
    ]

    for element, desc, reason, example in pure_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    add_section_divider(story)
    story.append(PageBreak())

    # ---------- FRAMEWORK 7: PAS ----------
    story.append(Paragraph("2.7 PAS - Pain Agitate Solution", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> The classic direct response framework that identifies a pain point, makes it feel "
        "more urgent, then presents your solution. Simple but extremely effective when done well.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Health/wellness products, anxiety/stress solutions, urgent problems, "
        "products that address emotional pain.", styles['CustomBody']))

    story.append(Paragraph("The PAS Framework Structure:", styles['FrameworkTitle']))

    pas_elements = [
        ("<b>P - Problem:</b>",
         "Address a core pain point with emotional, visceral language.",
         "WHY IT WORKS: Emotional language triggers the amygdala. People feel the pain, not just understand it.",
         "Example: 'My anxiety attacks used to leave me gasping for air, feeling like I was drowning.'"),

        ("<b>A - Agitate:</b>",
         "Explain how the pain affects them on a deeper emotional level. Intensify the feeling.",
         "WHY IT WORKS: Agitation creates urgency. If the pain isn't severe enough, there's no motivation to solve it now.",
         "Example: 'Deep breathing alone never seemed to help that chest-tightening panic. My breathing would always feel so weak.'"),

        ("<b>S - Solution:</b>",
         "Present your product with a unique mechanism and immediate payoff.",
         "WHY IT WORKS: After feeling the pain acutely, the solution feels like relief. Speed of result adds credibility.",
         "Example: 'MyLungBuddy has a unique dual resistance system that trains both inhale AND exhale muscles. Within 10 breaths, my heart slowed and my mind cleared.'")
    ]

    for element, desc, reason, example in pas_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    story.append(Paragraph("Psychological Triggers in PAS:", styles['FrameworkTitle']))
    story.append(Paragraph("- <b>Loss Aversion:</b> 'This will always be your reality' (if you don't act)", styles['BulletText']))
    story.append(Paragraph("- <b>Social Proof Gap:</b> 'Others cope - why can't you?'", styles['BulletText']))
    story.append(Paragraph("- <b>Certainty Anchor:</b> 'This WILL work for you'", styles['BulletText']))
    story.append(Paragraph("- <b>Identity Shift:</b> 'From victim to prepared warrior'", styles['BulletText']))

    add_section_divider(story)

    # ---------- FRAMEWORK 8: UGLY ADS ----------
    story.append(Paragraph("2.8 UGLY ADS - The Anti-Polish Approach", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework deliberately embraces low-production value, raw visuals, and "
        "blunt messaging. It stands out precisely because it DOESN'T look like an ad.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Saturated markets, authenticity-focused brands, low-budget testing, "
        "standing out from polished competitors.", styles['CustomBody']))

    story.append(Paragraph("The UGLY Ad Builder - 3 Questions:", styles['FrameworkTitle']))

    ugly_elements = [
        ("<b>1. How can I make this SIMPLER?</b>",
         "Strip complexity until it hurts. Can you say it in 5 words or less?",
         "WHY IT WORKS: Simple cuts through. In a world of complex messaging, blunt simplicity stands out.",
         "Before: 'Our journal helps you process emotions through CBT techniques.' After: 'ANGER JOURNAL -> THERAPIST VIDS + CBT PROMPTS -> CALM'"),

        ("<b>2. How can I show this CHEAPLY?</b>",
         "Embrace 'poor' production. Phone camera, natural lighting, MS Paint graphics.",
         "WHY IT WORKS: Low production signals authenticity. Overproduced = skepticism. Raw = trustworthy.",
         "Before: High-res chef with blender. After: Selfie of exhausted mom dumping powder into water while toddler screams. Text: '30 SECONDS -> LUNCH DONE.'"),

        ("<b>3. What's the OPPOSITE of competitors?</b>",
         "What would make your creative director cry? What rule can you break?",
         "WHY IT WORKS: Pattern interruption. When everyone zigs, zagging gets attention.",
         "Competitors: 'Find your dream career!' You: 'HATE YOUR BOSS? CLICK HERE TO STEAL HIS JOB.'")
    ]

    for element, desc, reason, example in ugly_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    add_section_divider(story)
    story.append(PageBreak())

    # ---------- FRAMEWORK 9: PROVE ----------
    story.append(Paragraph("2.9 Founder Objections - PROVE Framework", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework directly confronts skepticism by naming doubts out loud and crushing "
        "them with proof. It's founder-led but focused on overcoming objections.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Overcoming market skepticism, B2B products, innovative solutions, "
        "products that sound 'too good to be true'.", styles['CustomBody']))

    story.append(Paragraph("The PROVE Framework Structure:", styles['FrameworkTitle']))

    prove_elements = [
        ("<b>P - Problem (Stark Reality Hook):</b>",
         "Lead with an undeniable, painful truth.",
         "WHY IT WORKS: Starting with harsh reality establishes credibility. You're not sugar-coating.",
         "Example: 'They said it was impossible to fix South Africa's broken security system.'"),

        ("<b>R - Reframe (Founder's Credibility):</b>",
         "Contrast critics with your identity and expertise.",
         "WHY IT WORKS: Establishes authority. You're not just anyone - you have unique perspective/skills.",
         "Example: 'But we're builders...'"),

        ("<b>O - Objection (Name the Doubt):</b>",
         "Voice the specific skepticism you overcame.",
         "WHY IT WORKS: Naming objections takes their power away. It shows you understand and have answers.",
         "Example: 'Everyone said connecting thousands of WhatsApp groups was impossible. That communities would never work together at this scale.'"),

        ("<b>V - Victory (Proof):</b>",
         "Crush doubt with tangible, specific results.",
         "WHY IT WORKS: Results silence critics. Numbers and outcomes are undeniable.",
         "Example: 'But in just 4 months, we proved them wrong.'"),

        ("<b>E - Expand (Bigger Vision):</b>",
         "Pivot to the bigger ambition that aligns with buyer values.",
         "WHY IT WORKS: Shows you're not done. Creates opportunity for viewers to be part of something bigger.",
         "Example: 'And we're just getting started. Colombia, Brazil, Mexico - they all have the same problem.'")
    ]

    for element, desc, reason, example in prove_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    add_section_divider(story)

    # ---------- FRAMEWORK 10: SHOW ----------
    story.append(Paragraph("2.10 Us VS Them - SHOW Framework", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework creates a direct, visual competition between your product and "
        "an alternative (or everyday task). It proves superiority through demonstration.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Comparison ads, product demonstrations, speed/performance claims, "
        "products with clear measurable advantages.", styles['CustomBody']))

    story.append(Paragraph("The SHOW Framework Structure:", styles['FrameworkTitle']))

    show_elements = [
        ("<b>S - Set the challenge:</b>",
         "Pose a high-stakes challenge that demonstrates your product's strength.",
         "WHY IT WORKS: Challenges create tension and curiosity. Will they succeed?",
         "Example: 'Can I load 5 magazines before my oatmeal cooks?'"),

        ("<b>H - Head-to-head showdown:</b>",
         "Visually pit your product against the alternative. Use split-screen if possible.",
         "WHY IT WORKS: Visual proof is undeniable. Seeing is believing.",
         "Example: '[Split screen: Microwave counting down / Shooter loading magazines smoothly]'"),

        ("<b>O - Outcome & Why:</b>",
         "Reveal the winner and explain the features that enabled the win.",
         "WHY IT WORKS: The outcome satisfies curiosity; the why educates on product benefits.",
         "Example: 'Boom! 5 full magazines loaded before breakfast. The ETS Speedloader makes it easy and works with nearly every pistol magazine.'"),

        ("<b>W - Win & CTA:</b>",
         "Connect the victory to the viewer's benefit with 'if...then' logic.",
         "WHY IT WORKS: Translates the demo into personal benefit for the viewer.",
         "Example: 'So if loading your mags faster than your oatmeal cooks sounds good, grab your ETS Speedloader today.'")
    ]

    for element, desc, reason, example in show_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    add_section_divider(story)
    story.append(PageBreak())

    # ---------- FRAMEWORK 11: TRIPLE G ----------
    story.append(Paragraph("2.11 Triple G Framework - Goal, Gap, Gains", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> A simple but powerful framework that taps into aspirations, reveals what's missing, "
        "and shows how your product bridges the gap to achieve the desired transformation.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Seasonal campaigns, New Year/resolution marketing, goal-oriented audiences, "
        "transformation products.", styles['CustomBody']))

    story.append(Paragraph("The Triple G Framework Structure:", styles['FrameworkTitle']))

    tripleg_elements = [
        ("<b>G - Goal (Tap into aspiration):</b>",
         "Identify the specific outcome/transformation they want. Use year-specific language for urgency.",
         "WHY IT WORKS: Goals create emotional investment. Year-specific language adds time pressure.",
         "Example: 'Make hydration a habit in 2025' or 'Crush your fitness goals this year'"),

        ("<b>G - Gap (Reveal what's missing):</b>",
         "Expose why previous attempts failed. Position the missing tool/knowledge they didn't have.",
         "WHY IT WORKS: Explains past failure without blaming them. The 'gap' is what they were missing.",
         "Example: 'Current drinks are loaded with sugar and junk' or 'Exercise alone isn't enough without proper nutrition'"),

        ("<b>G - Gains (Show transformation):</b>",
         "Present your product as the bridge that closes the gap. Stack proof that it works.",
         "WHY IT WORKS: Connects aspiration to action. Your product = achieving the goal.",
         "Example: 'Zero sugar, zero junk electrolyte solution' or 'ButcherBox: 100% grass-fed beef, wild-caught seafood delivered to your door'")
    ]

    for element, desc, reason, example in tripleg_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    story.append(Paragraph("5 Hook Variations Using Triple G:", styles['FrameworkTitle']))
    story.append(Paragraph("1. <b>Goal-Question Hook:</b> '[Goal outcome]? Let's change that for 2025'", styles['BulletText']))
    story.append(Paragraph("2. <b>Gap-Reveal Hook:</b> 'Still failing at [goal] because you're missing this'", styles['BulletText']))
    story.append(Paragraph("3. <b>Tool-Bridge Hook:</b> 'The BEST tool to achieve [goal outcome]'", styles['BulletText']))
    story.append(Paragraph("4. <b>Habit-Gap Hook:</b> 'Make [goal] a habit with [missing piece]'", styles['BulletText']))
    story.append(Paragraph("5. <b>Year-Goal Hook:</b> 'Your 2025 [goal] starts with fixing this gap'", styles['BulletText']))

    add_section_divider(story)

    # ---------- FRAMEWORK 12: TEASE ----------
    story.append(Paragraph("2.12 Curiosity Loop - TEASE Framework", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHAT IT IS:</b> This framework creates a puzzle that can only be solved by watching the entire ad. "
        "It opens with an impossible/surprising claim and resolves it cleverly at the end.",
        styles['CustomBody']
    ))

    story.append(Paragraph("<b>BEST FOR:</b> Valentine's Day campaigns, special occasions, luxury/lifestyle products, "
        "any product where storytelling enhances perceived value.", styles['CustomBody']))

    story.append(Paragraph("The TEASE Framework Structure:", styles['FrameworkTitle']))

    tease_elements = [
        ("<b>T - Tease:</b>",
         "Create curiosity with an impossible or surprising claim.",
         "WHY IT WORKS: Cognitive dissonance demands resolution. The viewer MUST keep watching to understand.",
         "Example: 'I got my boyfriend a Valentine's gift for free.'"),

        ("<b>E - Engage:</b>",
         "Build story context and journey. Introduce the product naturally.",
         "WHY IT WORKS: Story builds emotional investment. The viewer is now part of a narrative.",
         "Example: 'So I went on that fishing date with my boyfriend and needed that extra oomph. So of course I used my favorite perfume from The Essence Vault.'"),

        ("<b>A - Advantage:</b>",
         "Show benefits and value within the story.",
         "WHY IT WORKS: Benefits feel organic when woven into narrative, not forced.",
         "Example: 'I swear by this stuff. It's so affordable and long lasting. My boyfriend was all over me. He kept asking how much I spent.'"),

        ("<b>S - Satisfy:</b>",
         "Resolve the curiosity loop cleverly.",
         "WHY IT WORKS: The payoff rewards the viewer for watching. It's satisfying and memorable.",
         "Example: 'He started saying because I saved so much money, I could pay for the date. The 'free gift' was the date itself!'"),

        ("<b>E - Encourage:</b>",
         "Call to action with urgency and bonus.",
         "WHY IT WORKS: After the emotional payoff, action feels natural.",
         "Example: 'Get 30% off plus a free gift worth up to 15 pounds this Valentine's Day.'")
    ]

    for element, desc, reason, example in tease_elements:
        story.append(Paragraph(element, styles['BulletText']))
        story.append(Paragraph(desc, styles['BulletText']))
        story.append(Paragraph(reason, styles['ReasonText']))
        story.append(Paragraph(f"<i>{example}</i>", styles['ExampleText']))
        story.append(Spacer(1, 5))

    story.append(Paragraph(
        "<b>WHY CURIOSITY LOOPS WORK:</b> They create a logical puzzle that can only be solved by watching "
        "the entire ad. This ensures high retention and engagement because viewers feel compelled to "
        "see the resolution.",
        styles['ReasonText']
    ))

    story.append(PageBreak())

    # ==================== SECTION 3: BRAND MESSAGING ====================
    story.append(Paragraph("3. BRAND MESSAGING GUIDELINES", styles['SectionHeader']))

    story.append(Paragraph(
        "Effective brand messaging in ads requires understanding both WHAT to say and HOW to say it. "
        "This section covers the key principles from the Ad Creators Lab for crafting compelling messages.",
        styles['CustomBody']
    ))

    # Hook Formulas
    story.append(Paragraph("3.1 Universal Hook Formulas", styles['SubsectionHeader']))

    story.append(Paragraph(
        "<b>WHY HOOKS MATTER:</b> You have 1-3 seconds to capture attention. The hook determines whether "
        "someone stops scrolling or keeps moving. Every framework should be tested with multiple hook variations.",
        styles['ReasonText']
    ))

    hook_formulas = [
        ("POV Hook", "POV: [Relatable situation]", "Creates immersion - viewer sees themselves in the scenario"),
        ("Question Hook", "[Pain point]? Here's what actually works", "Engages by asking what they're already wondering"),
        ("Contrarian Hook", "Everyone says [common belief] - they're wrong", "Pattern interruption through disagreement"),
        ("Identity Hook", "If you're a [identity] who [struggle], this is for you", "Qualifies viewer and creates belonging"),
        ("Curiosity Gap Hook", "[Surprising claim] - here's how", "Opens a loop that must be closed"),
        ("List Hook", "Top [number] reasons [problem exists]", "Promises organized, digestible information"),
        ("Authority Hook", "Why do [experts] swear by [solution]?", "Borrows trust from authority figures"),
        ("Time-Specific Hook", "Your 2025 [goal] starts with this", "Creates urgency with year-specific language")
    ]

    hook_table = [["Hook Type", "Formula", "Why It Works"]]
    for name, formula, why in hook_formulas:
        hook_table.append([name, formula, why])

    table = Table(hook_table, colWidths=[1.5*inch, 2.5*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(table)

    story.append(Spacer(1, 15))

    # Messaging Structures
    story.append(Paragraph("3.2 Messaging Structure by Goal", styles['SubsectionHeader']))

    story.append(Paragraph("<b>For Building Authority/Trust:</b>", styles['FrameworkTitle']))
    story.append(Paragraph("- Lead with expert endorsements or study citations", styles['BulletText']))
    story.append(Paragraph("- Use phrases like 'Scientists discovered...', 'Studies show...', 'Experts recommend...'", styles['BulletText']))
    story.append(Paragraph("- Include specific numbers and statistics (specificity = credibility)", styles['BulletText']))
    story.append(Paragraph("- Reference clinical trials, peer-reviewed research, or industry data", styles['BulletText']))
    story.append(Paragraph(
        "WHY: Authority messaging bypasses skepticism. People trust experts more than brands.",
        styles['ReasonText']
    ))

    story.append(Paragraph("<b>For Emotional Connection:</b>", styles['FrameworkTitle']))
    story.append(Paragraph("- Mirror customer frustrations with specific scenarios they recognize", styles['BulletText']))
    story.append(Paragraph("- Use 'I' statements and first-person narrative for relatability", styles['BulletText']))
    story.append(Paragraph("- Show vulnerability and real struggles (not just success)", styles['BulletText']))
    story.append(Paragraph("- End with transformation/success to create hope", styles['BulletText']))
    story.append(Paragraph(
        "WHY: Emotional messages stick. Logic makes people think; emotion makes people act.",
        styles['ReasonText']
    ))

    story.append(Paragraph("<b>For Urgency/Action:</b>", styles['FrameworkTitle']))
    story.append(Paragraph("- Use year-specific language ('Make 2025 your year of...')", styles['BulletText']))
    story.append(Paragraph("- Include limited-time offers or scarcity indicators", styles['BulletText']))
    story.append(Paragraph("- Add risk reversal (money-back guarantees, free trials)", styles['BulletText']))
    story.append(Paragraph("- Create FOMO with social proof ('Thousands are already...')", styles['BulletText']))
    story.append(Paragraph(
        "WHY: Urgency overcomes procrastination. Without urgency, 'later' becomes 'never'.",
        styles['ReasonText']
    ))

    story.append(Spacer(1, 10))

    # Brand Voice
    story.append(Paragraph("3.3 Brand Voice Principles", styles['SubsectionHeader']))

    voice_principles = [
        ("<b>Authentic:</b>", "Use raw, relatable language. Avoid corporate-speak. Say things how a real person would say them."),
        ("<b>Direct:</b>", "Simple words, short sentences, bullet points. Don't make people work to understand you."),
        ("<b>Proof-driven:</b>", "Always back claims with evidence. Social proof, studies, results - never make unsubstantiated claims."),
        ("<b>Identity-focused:</b>", "Address WHO the customer is, not just what they want. 'If you're a busy dad...' not 'For anyone who...'"),
        ("<b>Benefit-led:</b>", "Lead with what they GET, not what it IS. Features tell, benefits sell.")
    ]

    for principle, desc in voice_principles:
        story.append(Paragraph(f"{principle} {desc}", styles['BulletText']))

    story.append(Spacer(1, 10))

    story.append(Paragraph("Key Phrases to Use:", styles['FrameworkTitle']))
    phrases = [
        "'Here's the truth...' - Signals you're about to cut through the noise",
        "'Let's be honest...' - Creates intimacy and trust",
        "'Unlike [competitor approach]...' - Differentiates without naming competitors",
        "'The difference was immediate...' - Speed of results builds credibility",
        "'I'm not the only one who loves this...' - Introduces social proof naturally",
        "'And you can too...' - Bridges from proof to possibility for the viewer"
    ]
    for phrase in phrases:
        story.append(Paragraph(f"- {phrase}", styles['BulletText']))

    story.append(PageBreak())

    # ==================== SECTION 4: AUDIENCES ====================
    story.append(Paragraph("4. AUDIENCE TARGETING STRATEGIES", styles['SectionHeader']))

    story.append(Paragraph(
        "Not every framework works for every audience. Understanding where your target audience is in their "
        "awareness journey is crucial for selecting the right approach.",
        styles['CustomBody']
    ))

    story.append(Paragraph("4.1 The 5 Audience Types", styles['SubsectionHeader']))

    # Audience Type 1
    story.append(Paragraph("<b>A. Pain-Aware Audiences</b>", styles['FrameworkTitle']))
    story.append(Paragraph("<b>Who they are:</b> People actively experiencing problems but haven't found a solution yet.", styles['BulletText']))
    story.append(Paragraph("<b>Best frameworks:</b> PAS, Listicle (CURE), SIMPLE", styles['BulletText']))
    story.append(Paragraph("<b>Messaging focus:</b>", styles['BulletText']))
    story.append(Paragraph("- Specific pain scenarios they recognize", styles['BulletText']))
    story.append(Paragraph("- Failed solutions they've already tried", styles['BulletText']))
    story.append(Paragraph("- Immediate relief promises", styles['BulletText']))
    story.append(Paragraph(
        "WHY THESE FRAMEWORKS: Pain-aware audiences respond to messaging that validates their struggle "
        "and shows you understand their specific situation. PAS and Listicle frameworks excel at this.",
        styles['ReasonText']
    ))

    # Audience Type 2
    story.append(Paragraph("<b>B. Solution-Aware Audiences</b>", styles['FrameworkTitle']))
    story.append(Paragraph("<b>Who they are:</b> People who know solutions exist but haven't found the right one for them.", styles['BulletText']))
    story.append(Paragraph("<b>Best frameworks:</b> DISRUPT, SHOW (Us VS Them), Industry Contrarian", styles['BulletText']))
    story.append(Paragraph("<b>Messaging focus:</b>", styles['BulletText']))
    story.append(Paragraph("- Why alternative solutions fail", styles['BulletText']))
    story.append(Paragraph("- Your unique differentiators", styles['BulletText']))
    story.append(Paragraph("- Proof of superiority (comparisons, demos)", styles['BulletText']))
    story.append(Paragraph(
        "WHY THESE FRAMEWORKS: Solution-aware audiences need to understand why YOUR solution is different "
        "and better. Comparison and contrarian frameworks address this directly.",
        styles['ReasonText']
    ))

    # Audience Type 3
    story.append(Paragraph("<b>C. Identity-Based Audiences</b>", styles['FrameworkTitle']))
    story.append(Paragraph("<b>Who they are:</b> People who identify strongly with specific groups or lifestyles.", styles['BulletText']))
    story.append(Paragraph("<b>Best frameworks:</b> Bandwagon Effect, SIMPLE, FOUNDER", styles['BulletText']))
    story.append(Paragraph("<b>Messaging focus:</b>", styles['BulletText']))
    story.append(Paragraph("- 'If you're a [identity]...' language", styles['BulletText']))
    story.append(Paragraph("- What experts/peers in their group are doing", styles['BulletText']))
    story.append(Paragraph("- Tribe/community belonging", styles['BulletText']))
    story.append(Paragraph(
        "WHY THESE FRAMEWORKS: Identity-based audiences respond to messaging that speaks to who they are, "
        "not just what they want. Social proof from their 'tribe' is especially powerful.",
        styles['ReasonText']
    ))

    # Audience Type 4
    story.append(Paragraph("<b>D. Aspiration-Driven Audiences</b>", styles['FrameworkTitle']))
    story.append(Paragraph("<b>Who they are:</b> People motivated by goals and desired future states.", styles['BulletText']))
    story.append(Paragraph("<b>Best frameworks:</b> Triple G, TEASE, FOUNDER", styles['BulletText']))
    story.append(Paragraph("<b>Messaging focus:</b>", styles['BulletText']))
    story.append(Paragraph("- Year-specific goals and resolutions", styles['BulletText']))
    story.append(Paragraph("- Transformation stories", styles['BulletText']))
    story.append(Paragraph("- Vision alignment with their aspirations", styles['BulletText']))
    story.append(Paragraph(
        "WHY THESE FRAMEWORKS: Aspiration-driven audiences respond to messaging about who they could become, "
        "not just solving current problems. Goal-oriented frameworks tap into this motivation.",
        styles['ReasonText']
    ))

    # Audience Type 5
    story.append(Paragraph("<b>E. Skeptical/Analytical Audiences</b>", styles['FrameworkTitle']))
    story.append(Paragraph("<b>Who they are:</b> People who need substantial proof before making decisions.", styles['BulletText']))
    story.append(Paragraph("<b>Best frameworks:</b> PROVE, DISRUPT, CURE", styles['BulletText']))
    story.append(Paragraph("<b>Messaging focus:</b>", styles['BulletText']))
    story.append(Paragraph("- Clinical studies and research", styles['BulletText']))
    story.append(Paragraph("- Expert endorsements", styles['BulletText']))
    story.append(Paragraph("- Data, statistics, and specific numbers", styles['BulletText']))
    story.append(Paragraph("- Risk reversal (money-back guarantees)", styles['BulletText']))
    story.append(Paragraph(
        "WHY THESE FRAMEWORKS: Skeptical audiences won't buy on emotion alone. They need evidence "
        "and risk mitigation. Evidence-heavy frameworks overcome their objections.",
        styles['ReasonText']
    ))

    story.append(Spacer(1, 15))

    # Audience Matrix
    story.append(Paragraph("4.2 Audience Segmentation Matrix", styles['SubsectionHeader']))

    matrix_data = [
        ["Audience Type", "Pain Level", "Awareness", "Best Frameworks"],
        ["Cold Traffic", "Low", "Unaware", "Bandwagon, TEASE"],
        ["Warm Traffic", "Medium", "Problem-aware", "PAS, Listicle"],
        ["Hot Traffic", "High", "Solution-aware", "SHOW, PROVE"],
        ["Retargeting", "Variable", "Brand-aware", "FOUNDER, Triple G"]
    ]

    matrix_table = Table(matrix_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 2.5*inch])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(matrix_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "<b>KEY INSIGHT:</b> The same product may need different frameworks for different funnel stages. "
        "A cold audience needs education and social proof (Bandwagon); a retargeting audience needs "
        "reassurance and urgency (Triple G, FOUNDER).",
        styles['ReasonText']
    ))

    story.append(PageBreak())

    # ==================== SECTION 5: STRATEGIES ====================
    story.append(Paragraph("5. IMPLEMENTATION STRATEGIES", styles['SectionHeader']))

    story.append(Paragraph(
        "The Ad Creators Lab emphasizes that great ads come from great research and systematic testing. "
        "Here are the key strategies for implementing these frameworks effectively.",
        styles['CustomBody']
    ))

    # Strategy 1
    story.append(Paragraph("5.1 Research-First Approach", styles['SubsectionHeader']))
    story.append(Paragraph(
        "<b>THE PRINCIPLE:</b> Never create ads without first understanding your customer deeply. "
        "The Customer Research Protocol should be completed before any creative work begins.",
        styles['CustomBody']
    ))

    story.append(Paragraph("Research Protocol Steps:", styles['FrameworkTitle']))
    story.append(Paragraph("1. Complete Customer Research Protocol (understand pain points, desires, language)", styles['BulletText']))
    story.append(Paragraph("2. Understand Market Awareness levels (are they unaware, problem-aware, or solution-aware?)", styles['BulletText']))
    story.append(Paragraph("3. Use tools like Adnova to identify winning concepts in your market", styles['BulletText']))
    story.append(Paragraph("4. Analyze ad spend data - NOT 'longest running' ads", styles['BulletText']))

    story.append(Paragraph(
        "<b>CRITICAL INSIGHT:</b> Don't copy 'longest running' ads. These are often lowest-funnel retargeting "
        "ads that only work for warm audiences. Instead, analyze ad spend data to find what's actually "
        "performing across the full funnel.",
        styles['ReasonText']
    ))

    # Strategy 2
    story.append(Paragraph("5.2 Hook Variation Testing", styles['SubsectionHeader']))
    story.append(Paragraph(
        "<b>THE PRINCIPLE:</b> The hook is the most important part of any ad. Test multiple hook variations "
        "for every piece of creative.",
        styles['CustomBody']
    ))

    story.append(Paragraph("For every ad, create at least 5 hook variations:", styles['FrameworkTitle']))
    story.append(Paragraph("1. POV style hook ('POV: It's 7pm and your mascara still looks perfect')", styles['BulletText']))
    story.append(Paragraph("2. Question hook ('Why isn't your cellulite fading?')", styles['BulletText']))
    story.append(Paragraph("3. Listicle hook ('Top 3 reasons your skin routine isn't working')", styles['BulletText']))
    story.append(Paragraph("4. Curiosity gap hook ('I got my boyfriend a Valentine's gift for free')", styles['BulletText']))
    story.append(Paragraph("5. Identity-focused hook ('If you're a busy dad who hates skincare routines...')", styles['BulletText']))

    story.append(Paragraph(
        "<b>WHY 5 HOOKS:</b> The same body content can perform drastically differently with different hooks. "
        "Testing 5 variations helps you find what resonates with your specific audience quickly.",
        styles['ReasonText']
    ))

    # Strategy 3
    story.append(Paragraph("5.3 Framework Stacking", styles['SubsectionHeader']))
    story.append(Paragraph(
        "<b>THE PRINCIPLE:</b> Combine elements from multiple frameworks for maximum impact.",
        styles['CustomBody']
    ))

    story.append(Paragraph("Example Framework Stack:", styles['FrameworkTitle']))
    story.append(Paragraph("- Lead with TEASE curiosity hook", styles['BulletText']))
    story.append(Paragraph("- Build body with PAS structure (Pain - Agitate - Solution)", styles['BulletText']))
    story.append(Paragraph("- Close with SIMPLE escape CTA (identity-focused call to action)", styles['BulletText']))

    story.append(Paragraph(
        "WHY IT WORKS: Each framework has strengths. Curiosity hooks get attention, PAS builds desire, "
        "and identity CTAs drive action. Combining them creates a complete persuasion sequence.",
        styles['ReasonText']
    ))

    # Strategy 4
    story.append(Paragraph("5.4 Proof Stacking", styles['SubsectionHeader']))
    story.append(Paragraph(
        "<b>THE PRINCIPLE:</b> Layer multiple types of proof to build undeniable credibility.",
        styles['CustomBody']
    ))

    story.append(Paragraph("The 4 Types of Proof:", styles['FrameworkTitle']))
    story.append(Paragraph("1. <b>Social Proof:</b> Customer testimonials, reviews, user counts", styles['BulletText']))
    story.append(Paragraph("2. <b>Expert Proof:</b> Endorsements, studies, clinical trials, certifications", styles['BulletText']))
    story.append(Paragraph("3. <b>Demo Proof:</b> Live results, before/after, challenges", styles['BulletText']))
    story.append(Paragraph("4. <b>Statistical Proof:</b> Numbers, percentages, timelines", styles['BulletText']))

    story.append(Paragraph(
        "WHY STACK PROOF: Different people trust different types of evidence. By stacking multiple proof "
        "types, you cover all bases and create cumulative credibility.",
        styles['ReasonText']
    ))

    # Strategy 5
    story.append(Paragraph("5.5 UGLY Ads Strategy", styles['SubsectionHeader']))
    story.append(Paragraph(
        "<b>THE PRINCIPLE:</b> Sometimes low-production, raw content outperforms polished creative.",
        styles['CustomBody']
    ))

    story.append(Paragraph("When to use UGLY ads:", styles['FrameworkTitle']))
    story.append(Paragraph("- In saturated markets where everyone looks the same", styles['BulletText']))
    story.append(Paragraph("- For authenticity-focused brand positioning", styles['BulletText']))
    story.append(Paragraph("- During cost-conscious testing phases", styles['BulletText']))
    story.append(Paragraph("- When competitors are overly polished", styles['BulletText']))

    story.append(Paragraph(
        "WHY UGLY WORKS: Overproduced ads trigger skepticism ('this is clearly marketing'). Raw, authentic "
        "content triggers trust ('this feels like a real person sharing'). Pattern interruption also plays "
        "a role - ugly stands out when everything else is polished.",
        styles['ReasonText']
    ))

    # Strategy 6
    story.append(Paragraph("5.6 AI-Assisted Production", styles['SubsectionHeader']))
    story.append(Paragraph(
        "<b>THE PRINCIPLE:</b> Use AI tools to scale content production while maintaining quality.",
        styles['CustomBody']
    ))

    story.append(Paragraph("AI Production Tools from the Course:", styles['FrameworkTitle']))
    story.append(Paragraph("- <b>Voice overs:</b> AI voice generation for scalable audio", styles['BulletText']))
    story.append(Paragraph("- <b>B-roll:</b> AI-generated b-roll footage and images", styles['BulletText']))
    story.append(Paragraph("- <b>Character consistency:</b> Max Fusion method for consistent AI characters", styles['BulletText']))
    story.append(Paragraph("- <b>Script generation:</b> ChatGPT/Claude for initial script drafts", styles['BulletText']))
    story.append(Paragraph("- <b>Arcads:</b> AI avatar video generation", styles['BulletText']))

    story.append(PageBreak())

    # ==================== SECTION 6: PLANNING ====================
    story.append(Paragraph("6. CAMPAIGN PLANNING & STRUCTURE", styles['SectionHeader']))

    story.append(Paragraph("6.1 4-Phase Campaign Planning Framework", styles['SubsectionHeader']))

    # Phase 1
    story.append(Paragraph("<b>PHASE 1: RESEARCH (Week 1)</b>", styles['FrameworkTitle']))
    story.append(Paragraph("[ ] Complete Customer Research Protocol", styles['BulletText']))
    story.append(Paragraph("[ ] Analyze market awareness levels", styles['BulletText']))
    story.append(Paragraph("[ ] Use Adnova to find winning concepts", styles['BulletText']))
    story.append(Paragraph("[ ] Identify competitor ad spend patterns", styles['BulletText']))
    story.append(Paragraph("[ ] Document audience research findings", styles['BulletText']))
    story.append(Paragraph(
        "OUTCOME: Clear understanding of who you're targeting and what messaging will resonate.",
        styles['ReasonText']
    ))

    # Phase 2
    story.append(Paragraph("<b>PHASE 2: SCRIPT DEVELOPMENT (Week 2)</b>", styles['FrameworkTitle']))
    story.append(Paragraph("[ ] Select 2-3 frameworks based on audience type", styles['BulletText']))
    story.append(Paragraph("[ ] Write full scripts using framework structure", styles['BulletText']))
    story.append(Paragraph("[ ] Create 5 hook variations per script", styles['BulletText']))
    story.append(Paragraph("[ ] Include B-roll suggestions", styles['BulletText']))
    story.append(Paragraph("[ ] Add text overlay recommendations", styles['BulletText']))
    story.append(Paragraph(
        "OUTCOME: Complete creative briefs ready for production with multiple testable elements.",
        styles['ReasonText']
    ))

    # Phase 3
    story.append(Paragraph("<b>PHASE 3: PRODUCTION (Week 3)</b>", styles['FrameworkTitle']))
    story.append(Paragraph("[ ] UGC content shoots OR AI avatar generation", styles['BulletText']))
    story.append(Paragraph("[ ] AI voice over creation", styles['BulletText']))
    story.append(Paragraph("[ ] B-roll compilation", styles['BulletText']))
    story.append(Paragraph("[ ] Video editing and assembly", styles['BulletText']))
    story.append(Paragraph("[ ] Create multiple versions with different hooks", styles['BulletText']))
    story.append(Paragraph(
        "OUTCOME: Multiple ad variations ready for testing.",
        styles['ReasonText']
    ))

    # Phase 4
    story.append(Paragraph("<b>PHASE 4: LAUNCH & OPTIMIZATION</b>", styles['FrameworkTitle']))
    story.append(Paragraph("[ ] Launch with multiple creatives", styles['BulletText']))
    story.append(Paragraph("[ ] Test hook variations", styles['BulletText']))
    story.append(Paragraph("[ ] Monitor ad spend efficiency", styles['BulletText']))
    story.append(Paragraph("[ ] Scale winners, kill losers", styles['BulletText']))
    story.append(Paragraph("[ ] Iterate based on data", styles['BulletText']))
    story.append(Paragraph(
        "OUTCOME: Data-driven scaling of proven creative combinations.",
        styles['ReasonText']
    ))

    story.append(Spacer(1, 15))

    # Campaign Calendar
    story.append(Paragraph("6.2 Campaign Calendar Template", styles['SubsectionHeader']))

    calendar_data = [
        ["Week", "Focus", "Frameworks", "Output"],
        ["1", "Cold Audience", "Bandwagon, TEASE", "5 creatives"],
        ["2", "Warm Audience", "PAS, Listicle", "5 creatives"],
        ["3", "Hot Audience", "SHOW, PROVE", "5 creatives"],
        ["4", "Retargeting", "FOUNDER, Triple G", "3 creatives"]
    ]

    calendar_table = Table(calendar_data, colWidths=[0.8*inch, 1.5*inch, 2*inch, 1.5*inch])
    calendar_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(calendar_table)

    story.append(Spacer(1, 15))

    # Creative Brief Template
    story.append(Paragraph("6.3 Creative Brief Template", styles['SubsectionHeader']))

    story.append(Paragraph("<b>For Each Ad Creative:</b>", styles['FrameworkTitle']))
    story.append(Spacer(1, 5))

    brief_items = [
        "<b>1. Framework Selected:</b> [Name of framework]",
        "<b>2. Target Audience:</b> [Audience type and awareness level]",
        "<b>3. Hook Options:</b>",
        "   - Hook 1: _______________",
        "   - Hook 2: _______________",
        "   - Hook 3: _______________",
        "   - Hook 4: _______________",
        "   - Hook 5: _______________",
        "<b>4. Script Structure:</b>",
        "   - Opening (Hook): _______________",
        "   - Problem/Gap: _______________",
        "   - Solution Introduction: _______________",
        "   - Proof/Evidence: _______________",
        "   - CTA: _______________",
        "<b>5. Production Notes:</b>",
        "   - Video Type: [UGC / AI / Mixed]",
        "   - Length Target: [15s / 30s / 60s]",
        "   - B-roll Requirements: _______________",
        "   - Text Overlays: _______________",
        "<b>6. Success Metrics:</b>",
        "   - Target CTR: _______________",
        "   - Target CPA: _______________",
        "   - Test Budget: _______________"
    ]

    for item in brief_items:
        story.append(Paragraph(item, styles['BulletText']))

    story.append(PageBreak())

    # ==================== SECTION 7: QUICK REFERENCE ====================
    story.append(Paragraph("7. FRAMEWORK QUICK REFERENCE", styles['SectionHeader']))

    story.append(Paragraph(
        "Use this reference guide to quickly select the right framework for your situation.",
        styles['CustomBody']
    ))

    # Selection Guide
    story.append(Paragraph("7.1 Framework Selection by Situation", styles['SubsectionHeader']))

    selection_data = [
        ["Situation", "Recommended Framework", "Why"],
        ["New product launch", "Bandwagon Effect", "Leverage trend/movement energy"],
        ["Fighting skepticism", "DISRUPT / PROVE", "Address objections directly with evidence"],
        ["Educating market", "Listicle / PAS", "Organized info that validates struggles"],
        ["Brand storytelling", "FOUNDER", "Human connection through narrative"],
        ["Convenience messaging", "SIMPLE", "Position as easy shortcut"],
        ["Authenticity play", "PURE / UGLY ADS", "Raw, unpolished builds trust"],
        ["Comparison marketing", "SHOW (Us VS Them)", "Visual proof of superiority"],
        ["Goal-based campaigns", "Triple G", "Tap into aspirations"],
        ["Special occasions", "TEASE", "Curiosity loop with clever payoff"],
        ["Low-budget testing", "UGLY ADS", "Minimal production, maximum authenticity"],
        ["B2B products", "PROVE / FOUNDER", "Credibility through results"],
        ["Health/wellness", "PAS / Bandwagon", "Pain and social proof"]
    ]

    selection_table = Table(selection_data, colWidths=[1.8*inch, 1.8*inch, 2.5*inch])
    selection_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(selection_table)

    story.append(Spacer(1, 20))

    # Framework Acronyms
    story.append(Paragraph("7.2 Framework Acronym Reference", styles['SubsectionHeader']))

    acronym_data = [
        ["Framework", "Acronym", "Elements"],
        ["Bandwagon Effect", "CROWD", "Call out - Reject - Onboard - Wave proof - Direct"],
        ["Industry Contrarian", "DISRUPT", "Declassify - Industry fail - Solution - Reinforce - Upstage - Provide - Trigger"],
        ["Listicle", "CURE", "Curiosity - Uncover - Remedy - Evidence - Engage"],
        ["Founder-Led", "FOUNDER", "Feature - Opposing - Unlocking - Numbers - Destiny - Engage"],
        ["Convenience", "SIMPLE", "State - Identify - Minimal - Prove - Lifestyle - Escape"],
        ["Organic", "PURE", "Problem - Unfiltered - Real - Effortless"],
        ["Pain Framework", "PAS", "Problem - Agitate - Solution"],
        ["Low Production", "UGLY", "Unpolished - Gritty - Lean - Yelling-for-action"],
        ["Objection Crusher", "PROVE", "Problem - Reframe - Objection - Victory - Expand"],
        ["Comparison", "SHOW", "Set challenge - Head-to-head - Outcome - Win"],
        ["Goal-Based", "Triple G", "Goal - Gap - Gains"],
        ["Curiosity Loop", "TEASE", "Tease - Engage - Advantage - Satisfy - Encourage"]
    ]

    acronym_table = Table(acronym_data, colWidths=[1.3*inch, 1*inch, 3.8*inch])
    acronym_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(acronym_table)

    story.append(PageBreak())

    # ==================== SECTION 8: COMPLETE SCRIPTS ====================
    story.append(Paragraph("8. EXAMPLE FRAMEWORK SCRIPTS", styles['SectionHeader']))

    story.append(Paragraph(
        "Below are complete example scripts from the course showing each framework in action.",
        styles['CustomBody']
    ))

    # Example 1: Bandwagon
    story.append(Paragraph("8.1 Bandwagon Effect Example (Soothe Supps)", styles['SubsectionHeader']))
    story.append(Paragraph("<b>Product:</b> GHK-Cu peptide supplement for anti-aging", styles['BulletText']))
    story.append(Spacer(1, 5))

    bandwagon_script = """
<b>HOOK:</b> "Why do anti-aging experts swear by copper peptides over collagen? Here's the truth."

<b>CALL OUT THE MOVEMENT:</b> "Is GHK-CU just hyped up? Anti-aging experts think not."

<b>REJECT THE OLD WAY:</b> "Most people spend thousands on anti-aging creams and treatments, but your body already makes a natural compound called Copper Tripeptide-1 (GHK-Cu)."

<b>ONBOARD THE NEW WAY:</b> "And Soothe Supps puts this powerful compound into a peptide. It works at a cellular level to:
- Boost collagen production
- Enhance skin firmness
- Reduce fine lines
- Accelerate skin repair"

<b>WAVE THE PROOF:</b> "But this isn't just another 'special ingredient' that wellness influencers are hyping up. It's actually backed by clinical studies and results."

<b>DIRECT THE VIEWER:</b> "You can get it at Soothe Supps right now, to look and feel younger. Support younger-looking skin with GHK-CU."
"""
    story.append(Paragraph(bandwagon_script, styles['CustomBody']))

    # Example 2: SIMPLE
    story.append(Paragraph("8.2 SIMPLE Framework Example (Three Beacon Tallow Balm)", styles['SubsectionHeader']))
    story.append(Paragraph("<b>Product:</b> Tallow balm for busy dads with dry skin", styles['BulletText']))
    story.append(Spacer(1, 5))

    simple_script = """
<b>HOOK:</b> "If you're a busy dad and hate skincare routines, this is for you."

<b>IDENTIFY PAIN:</b> "As a dad, life moves fast. Between work, family, and everything in between, I rarely have time for complicated skin routines. But I couldn't keep ignoring my dry, cracked skin."

<b>MINIMAL SOLUTION:</b> "Which is why I started using this all-natural balm. I put it on my face in the morning, and since it's packed with grass-fed tallow, it locks in hydration for the whole day."

<b>PROVE:</b> "And the beeswax protects my skin from harsh weather, without feeling greasy. Plus my skin isn't always stinging from irritation anymore because the premium raw honey really soothes my skin."

<b>LIFESTYLE WIN:</b> "I love this balm because there's no fancy steps - you just apply it and boom, you're done."

<b>ESCAPE CTA:</b> "So if you're a dad and you're tired of your dry skin but don't wanna add a whole chore to your day, go grab this tallow balm now. It's all you need."
"""
    story.append(Paragraph(simple_script, styles['CustomBody']))

    add_section_divider(story)

    # Final Notes
    story.append(Paragraph("IMPLEMENTATION CHECKLIST", styles['SectionHeader']))

    story.append(Paragraph("<b>Immediate Actions:</b>", styles['FrameworkTitle']))
    story.append(Paragraph("[ ] Complete customer research protocol for your product", styles['BulletText']))
    story.append(Paragraph("[ ] Select 3 frameworks to test first based on your audience", styles['BulletText']))
    story.append(Paragraph("[ ] Create first batch of 5 hook variations", styles['BulletText']))
    story.append(Paragraph("[ ] Set up testing structure with clear metrics", styles['BulletText']))

    story.append(Paragraph("<b>Weekly Routine:</b>", styles['FrameworkTitle']))
    story.append(Paragraph("- Monday: Review ad performance data", styles['BulletText']))
    story.append(Paragraph("- Tuesday: Script new creatives based on learnings", styles['BulletText']))
    story.append(Paragraph("- Wednesday: Production/editing day", styles['BulletText']))
    story.append(Paragraph("- Thursday: Launch new tests", styles['BulletText']))
    story.append(Paragraph("- Friday: Analyze and optimize", styles['BulletText']))

    story.append(Paragraph("<b>Monthly Review Questions:</b>", styles['FrameworkTitle']))
    story.append(Paragraph("- Which frameworks performed best?", styles['BulletText']))
    story.append(Paragraph("- Which hooks won?", styles['BulletText']))
    story.append(Paragraph("- Which audience segments converted?", styles['BulletText']))
    story.append(Paragraph("- What's the winning creative formula?", styles['BulletText']))

    story.append(Spacer(1, 30))

    # Footer
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2c5282')))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Document generated from Ad Creators Lab (AI Ads That Scale) course content</b>",
        styles['CustomBody']
    ))
    story.append(Paragraph(
        f"Analysis Date: {datetime.now().strftime('%B %d, %Y')} | For: Ecommerce Manager Implementation",
        styles['CustomBody']
    ))

    # Build PDF
    doc.build(story)
    print(f"PDF created successfully: {filename}")
    return filename

if __name__ == "__main__":
    build_pdf()
