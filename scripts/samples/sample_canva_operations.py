#!/usr/bin/env python3
"""
Sample Script: Canva API Operations
Usage: python scripts/samples/sample_canva_operations.py
Requires: Canva API credentials in .env file
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

def check_canva_auth():
    """Step 1: Always check authentication first."""
    try:
        from canva_client import get_client
        client = get_client()
        if not client.access_token:
            print("ERROR: No Canva access token. Run: python scripts/oauth_flow.py")
            return None
        print("Canva authentication: OK")
        return client
    except Exception as e:
        print(f"ERROR: {e}")
        print("Make sure .env has CANVA_CLIENT_ID, CANVA_CLIENT_SECRET, CANVA_ACCESS_TOKEN")
        return None

def list_my_designs(client, limit=20):
    """Step 2: List designs in your account."""
    result = client.list_designs(limit=limit)
    designs = result.get("designs", [])

    print(f"\nFound {len(designs)} designs:")
    for i, d in enumerate(designs, 1):
        title = d.get("title", "Untitled")
        design_type = d.get("design_type", {}).get("type", "unknown")
        design_id = d.get("id")
        print(f"  {i}. [{design_type}] {title} (ID: {design_id})")

    return designs

def export_design(client, design_id, format_type="pdf"):
    """Step 3: Export a design."""
    print(f"\nExporting design {design_id} as {format_type}...")

    # Start export
    export_job = client.create_export(design_id=design_id, format_type=format_type)
    job_id = export_job.get("job", {}).get("id")
    print(f"Export job started: {job_id}")

    # Wait for completion
    result = client.wait_for_export(job_id)
    status = result.get("job", {}).get("status")

    if status == "completed":
        urls = result.get("job", {}).get("result", {}).get("urls", [])
        print(f"Export complete! Download URLs: {len(urls)}")
        for url_info in urls:
            print(f"  {url_info.get('url', 'N/A')[:80]}...")
        return urls
    else:
        print(f"Export failed: {status}")
        return []

def list_my_folders(client):
    """List folder structure."""
    result = client.list_folders()
    folders = result.get("folders", [])

    print(f"\nFound {len(folders)} folders:")
    for f in folders:
        print(f"  - {f.get('name', 'Unknown')} (ID: {f.get('id')})")

    return folders

if __name__ == "__main__":
    # === WORKFLOW ===
    # Step 1: Check auth
    client = check_canva_auth()
    if not client:
        print("\nFix authentication first, then re-run this script.")
        sys.exit(1)

    # Step 2: List designs
    designs = list_my_designs(client, limit=10)

    # Step 3: To export, uncomment and set design_id:
    # export_design(client, design_id="YOUR_DESIGN_ID", format_type="pdf")
