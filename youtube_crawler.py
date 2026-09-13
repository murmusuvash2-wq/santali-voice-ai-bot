#!/usr/bin/env python3
"""
YouTube Crawler for Santali Content
Downloads Santali songs, videos, news for training dataset
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeCrawler:
    """Crawl and download Santali content from YouTube"""
    
    def __init__(self, output_dir: str = "./santali_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Search queries for Santali content
        self.search_queries = [
            "Santali song",
            "Santali video",
            "Santali news",
            "Santali podcast",
            "Santali speech",
            "Santali traditional music",
            "Santali culture",
            "संताली गीत",
            "संताली वीडियो"
        ]
    
    def download_audio(self, url: str, output_file: str) -> bool:
        """Download audio from YouTube using yt-dlp"""
        try:
            logger.info(f"Downloading: {url}")
            
            cmd = [
                "yt-dlp",
                "-x",  # Extract audio
                "-f", "bestaudio/best",
                "-o", output_file,
                "--audio-format", "wav",
                "--audio-quality", "192",
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            
            if result.returncode == 0:
                logger.info(f"✅ Downloaded: {output_file}")
                return True
            else:
                logger.error(f"❌ Failed: {result.stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return False
    
    def search_youtube(self, query: str, max_results: int = 10) -> List[str]:
        """Search YouTube and get video URLs"""
        try:
            logger.info(f"🔍 Searching: {query}")
            
            cmd = [
                "yt-dlp",
                "--dump-json",
                "--no-warnings",
                f"ytsearch{max_results}:{query}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                urls = []
                
                for line in lines:
                    try:
                        data = json.loads(line)
                        url = f"https://youtube.com/watch?v={data['id']}"
                        urls.append(url)
                    except:
                        pass
                
                logger.info(f"Found {len(urls)} videos for '{query}'")
                return urls
            else:
                logger.error(f"Search failed: {result.stderr}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching YouTube: {e}")
            return []
    
    def crawl_and_download(self, max_per_query: int = 5) -> Dict[str, int]:
        """Crawl YouTube for Santali content and download"""
        
        stats = {
            "total_searched": 0,
            "total_downloaded": 0,
            "failed": 0
        }
        
        for query in self.search_queries:
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing: {query}")
            logger.info(f"{'='*60}")
            
            # Search
            urls = self.search_youtube(query, max_results=max_per_query)
            stats["total_searched"] += len(urls)
            
            # Download
            for idx, url in enumerate(urls, 1):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_query = query.replace(" ", "_").replace("/", "_")
                output_file = self.output_dir / f"{safe_query}_{idx}_{timestamp}.wav"
                
                if self.download_audio(url, str(output_file)):
                    stats["total_downloaded"] += 1
                else:
                    stats["failed"] += 1
        
        return stats

def main():
    """Main crawling pipeline"""
    print("=" * 80)
    print("🎵 Santali YouTube Crawler")
    print("=" * 80)
    
    crawler = YouTubeCrawler(output_dir="./santali_data")
    
    print("\n📥 Starting crawl...")
    print("This will download Santali songs, videos, news from YouTube\n")
    
    stats = crawler.crawl_and_download(max_per_query=3)
    
    print("\n" + "=" * 80)
    print("📊 Crawl Statistics:")
    print(f"   Total Searched: {stats['total_searched']}")
    print(f"   Total Downloaded: {stats['total_downloaded']}")
    print(f"   Failed: {stats['failed']}")
    print(f"   Output Directory: ./santali_data")
    print("=" * 80)

if __name__ == "__main__":
    main()
