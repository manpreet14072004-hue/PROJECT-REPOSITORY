#!/usr/bin/env python3
"""
NYC TLC Yellow Taxi Data Download Script
Downloads 2023 data (12 months) - approximately 1.5-2GB total
"""

import os
import sys
from pathlib import Path
import urllib.request
import urllib.error

def download_file(url, destination):
    """Download file with progress bar."""
    try:
        print(f"\nDownloading: {url}")
        
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(downloaded * 100.0 / total_size, 100)
                size_mb = total_size / (1024 * 1024)
                downloaded_mb = downloaded / (1024 * 1024)
                sys.stdout.write(f"\r  Progress: {percent:.1f}% ({downloaded_mb:.1f}/{size_mb:.1f} MB)")
                sys.stdout.flush()
        
        urllib.request.urlretrieve(url, destination, progress_hook)
        print(f"\n  ✓ Saved to: {destination}")
        return True
        
    except urllib.error.HTTPError as e:
        print(f"\n  ✗ HTTP Error {e.code}: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"\n  ✗ URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"\n  ✗ Error: {str(e)}")
        return False


def main():
    """Download NYC TLC Yellow Taxi data for 2023."""
    
    # Create data directory
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("NYC TLC Yellow Taxi Data Download")
    print("="*70)
    print(f"Years: 2022-2023 (24 months)")
    print(f"Destination: {data_dir.absolute()}")
    print(f"Expected size: ~1.5-2 GB total")
    print("="*70)
    
    # Base URL for NYC TLC data
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    
    # Download 2022 and 2023 data to ensure >1GB
    years = [2022, 2023]
    months = range(1, 13)  # January to December
    
    successful = 0
    failed = 0
    skipped = 0
    total_files = len(years) * len(months)
    file_counter = 0
    
    for year in years:
        for month in months:
            file_counter += 1
            filename = f"yellow_tripdata_{year}-{month:02d}.parquet"
            url = f"{base_url}/{filename}"
            destination = data_dir / filename
            
            # Skip if file already exists
            if destination.exists():
                file_size_mb = destination.stat().st_size / (1024 * 1024)
                print(f"\n[{file_counter}/{total_files}] {filename}")
                print(f"  ⊙ Already exists ({file_size_mb:.1f} MB) - skipping")
                skipped += 1
                continue
            
            print(f"\n[{file_counter}/{total_files}] {filename}")
            if download_file(url, destination):
                successful += 1
            else:
                failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("DOWNLOAD SUMMARY")
    print("="*70)
    print(f"Successful:  {successful}/{total_files}")
    print(f"Skipped:     {skipped}/{total_files} (already downloaded)")
    print(f"Failed:      {failed}/{total_files}")
    print("="*70)
    
    if successful + skipped == total_files:
        print("\n✓ All data files are ready!")
        print("\nNext steps:")
        print("1. Activate conda environment: conda activate project-env")
        print("2. Start Jupyter Lab: jupyter lab")
        print("3. Run notebooks in sequence: 1_data_ingestion.ipynb → 2_feature_engineering.ipynb → etc.")
    elif successful > 0:
        print(f"\n⚠ Partial download: {successful + skipped}/{total_files} files available")
        print("You can proceed with available data or retry failed downloads.")
    else:
        print("\n✗ Download failed!")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Verify firewall settings")
        print("3. Try manual download from: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")
        print("4. Place files in: data/raw/")
    
    # Calculate total size
    if successful + skipped > 0:
        total_size = sum(f.stat().st_size for f in data_dir.glob("*.parquet"))
        total_size_gb = total_size / (1024 ** 3)
        print(f"\nTotal data size: {total_size_gb:.2f} GB")
        
        if total_size_gb >= 1.0:
            print("✓ Dataset size requirement met (>1GB)")
        else:
            print("⚠ Dataset size below 1GB - consider downloading more months")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {str(e)}")
        sys.exit(1)
