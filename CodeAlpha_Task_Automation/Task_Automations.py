"""
✨ Task Automation Script - Three in One ✨
Enhanced with rich formatting, colors, and better UX
Fixed Windows Cloud File Provider Error
"""

import os
import shutil
import re
import requests
from pathlib import Path
from datetime import datetime
import sys
from time import sleep
import random

# Try to import rich for better formatting
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    from rich.prompt import Prompt, Confirm
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

# Color codes for fallback if rich is not available
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(text, color_code):
    """Fallback colored printing if rich is not available"""
    if RICH_AVAILABLE:
        rprint(text)
    else:
        print(f"{color_code}{text}{Colors.END}")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print attractive application header"""
    clear_screen()
    
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold cyan]✨ Task Automation Script ✨[/]\n"
            "[yellow]Three Tools in One: Images • Emails • Web Scraping[/]",
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print()
    else:
        print(f"\n{Colors.CYAN}{'='*60}")
        print(f"{Colors.BOLD}✨ Task Automation Script ✨{Colors.END}")
        print(f"{Colors.YELLOW}Three Tools in One: Images • Emails • Web Scraping{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_menu():
    """Print attractive main menu"""
    print_header()
    
    if RICH_AVAILABLE:
        # Create a table for menu options
        table = Table(title="[bold yellow]Main Menu[/]", show_header=False, box=None)
        table.add_column("Choice", style="cyan", width=8)
        table.add_column("Task", style="white", width=40)
        table.add_column("Description", style="dim", width=40)
        
        table.add_row(
            "[bold]1[/]", 
            "[green]📸 Move Image Files[/]", 
            "[dim]Move JPG/PNG files between folders[/]"
        )
        table.add_row(
            "[bold]2[/]", 
            "[blue]📧 Extract Email Addresses[/]", 
            "[dim]Extract emails from text files[/]"
        )
        table.add_row(
            "[bold]3[/]", 
            "[magenta]🌐 Scrape Webpage Title[/]", 
            "[dim]Scrape webpage information[/]"
        )
        table.add_row(
            "[bold]4[/]", 
            "[red]🚪 Exit Program[/]", 
            "[dim]Close the application[/]"
        )
        
        console.print(table)
        console.print()
    else:
        print(f"{Colors.BOLD}{'MAIN MENU':^60}{Colors.END}")
        print(f"{Colors.CYAN}{'-'*60}{Colors.END}")
        print(f"{Colors.GREEN}1. 📸 Move Image Files{Colors.END}")
        print("   Move JPG/PNG files between folders")
        print()
        print(f"{Colors.BLUE}2. 📧 Extract Email Addresses{Colors.END}")
        print("   Extract emails from text files")
        print()
        print(f"{Colors.MAGENTA}3. 🌐 Scrape Webpage Title{Colors.END}")
        print("   Scrape webpage information")
        print()
        print(f"{Colors.RED}4. 🚪 Exit Program{Colors.END}")
        print("   Close the application")
        print(f"{Colors.CYAN}{'-'*60}{Colors.END}")

def animated_progress(description="Processing..."):
    """Show animated progress indicator"""
    if RICH_AVAILABLE:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description, total=None)
            for _ in range(100):
                sleep(0.02)
                progress.update(task, advance=1)
    else:
        print(f"{description}", end="", flush=True)
        for _ in range(10):
            print(".", end="", flush=True)
            sleep(0.1)
        print()

def safe_file_move(source_path, destination_path, file):
    """
    Safely move a file with error handling for Windows Cloud Files
    """
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            # Check if file exists
            if not os.path.exists(source_path):
                return False, f"Source file not found: {file}"
            
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Handle duplicates
            counter = 1
            base_name, ext = os.path.splitext(file)
            original_dest = destination_path
            
            while os.path.exists(destination_path):
                new_name = f"{base_name}_{counter}{ext}"
                destination_path = os.path.join(os.path.dirname(original_dest), new_name)
                counter += 1
            
            # Try to move the file
            shutil.move(source_path, destination_path)
            return True, destination_path
            
        except PermissionError as e:
            if attempt < max_retries - 1:
                sleep(retry_delay)
                continue
            return False, f"Permission denied for file: {file}"
            
        except OSError as e:
            if "cloud" in str(e).lower() or "362" in str(e):
                # Cloud file provider error - try copy+delete method
                try:
                    shutil.copy2(source_path, destination_path)
                    os.remove(source_path)
                    return True, destination_path
                except Exception as copy_error:
                    if attempt < max_retries - 1:
                        sleep(retry_delay)
                        continue
                    return False, f"Cloud file error for {file}: {str(copy_error)}"
            else:
                if attempt < max_retries - 1:
                    sleep(retry_delay)
                    continue
                return False, f"Error moving {file}: {str(e)}"
                
        except Exception as e:
            if attempt < max_retries - 1:
                sleep(retry_delay)
                continue
            return False, f"Unexpected error for {file}: {str(e)}"
    
    return False, f"Failed to move {file} after {max_retries} attempts"

# ==================== TASK 1: Move Image Files ====================
def task1_move_image_files():
    """Task 1: Move all image files with attractive interface and error handling"""
    print_header()
    
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold green]📸 TASK 1: MOVE IMAGE FILES[/]\n"
            "[dim]Move JPG, JPEG, and PNG files between folders[/]",
            border_style="green"
        ))
        console.print()
    else:
        print(f"{Colors.GREEN}{'TASK 1: MOVE IMAGE FILES':^60}{Colors.END}")
        print(f"{Colors.GREEN}{'-'*60}{Colors.END}\n")
    
    # Get source folder with better prompt
    source_folder = Prompt.ask(
        "[cyan]📁 Enter source folder path[/]",
        default=os.getcwd()
    ) if RICH_AVAILABLE else input(f"{Colors.CYAN}📁 Enter source folder path (Enter for current):{Colors.END} ").strip() or os.getcwd()
    
    # Expand user directory shortcuts
    source_folder = os.path.expanduser(source_folder)
    
    if not os.path.exists(source_folder):
        print_colored(f"\n❌ Error: Source folder '{source_folder}' does not exist!", Colors.RED)
        input("\nPress Enter to continue...")
        return
    
    # Get destination folder
    default_dest = os.path.join(os.getcwd(), "Images")
    if RICH_AVAILABLE:
        destination_folder = Prompt.ask(
            "[cyan]📂 Enter destination folder[/]",
            default=default_dest
        )
    else:
        print(f"\n{Colors.CYAN}📂 Enter destination folder (Enter for 'Images'):{Colors.END}", end=" ")
        destination_folder = input().strip() or default_dest
    
    # Expand user directory shortcuts
    destination_folder = os.path.expanduser(destination_folder)
    
    # Show summary
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            f"[bold]📋 Operation Summary[/]\n\n"
            f"[cyan]Source:[/] {source_folder}\n"
            f"[cyan]Destination:[/] {destination_folder}\n"
            f"[cyan]File Types:[/] JPG, JPEG, PNG",
            border_style="yellow"
        ))
    else:
        print(f"\n{Colors.YELLOW}{'Operation Summary':^60}{Colors.END}")
        print(f"{Colors.YELLOW}{'-'*60}{Colors.END}")
        print(f"{Colors.CYAN}Source:{Colors.END} {source_folder}")
        print(f"{Colors.CYAN}Destination:{Colors.END} {destination_folder}")
        print(f"{Colors.CYAN}File Types:{Colors.END} JPG, JPEG, PNG")
        print(f"{Colors.YELLOW}{'-'*60}{Colors.END}")
    
    # Confirm action
    if RICH_AVAILABLE:
        proceed = Confirm.ask("\n✨ Proceed with moving image files?", default=True)
    else:
        proceed = input(f"\n{Colors.GREEN}✨ Proceed with moving image files? (y/n):{Colors.END} ").lower() == 'y'
    
    if not proceed:
        print_colored("\n🚫 Operation cancelled.", Colors.YELLOW)
        input("\nPress Enter to continue...")
        return
    
    # Execute the move operation
    try:
        animated_progress("🔍 Scanning for image files...")
        
        # Create destination folder
        Path(destination_folder).mkdir(parents=True, exist_ok=True)
        
        # Find image files
        image_extensions = ('.jpg', '.jpeg', '.png')
        image_files = []
        
        for file in os.listdir(source_folder):
            file_path = os.path.join(source_folder, file)
            if os.path.isfile(file_path) and file.lower().endswith(image_extensions):
                image_files.append(file)
        
        if not image_files:
            print_colored("\n📭 No JPG or PNG files found in the source folder!", Colors.YELLOW)
            input("\nPress Enter to continue...")
            return
        
        # Count files by type
        jpg_count = sum(1 for f in image_files if f.lower().endswith(('.jpg', '.jpeg')))
        png_count = sum(1 for f in image_files if f.lower().endswith('.png'))
        
        # Show found files
        if RICH_AVAILABLE:
            console.print(f"\n[green]✅ Found {len(image_files)} image file(s):[/]")
            console.print(f"   📷 [cyan]JPG/JPEG:[/] {jpg_count} file(s)")
            console.print(f"   🖼️  [cyan]PNG:[/] {png_count} file(s)")
        else:
            print(f"\n{Colors.GREEN}✅ Found {len(image_files)} image file(s):{Colors.END}")
            print(f"   📷 {Colors.CYAN}JPG/JPEG:{Colors.END} {jpg_count} file(s)")
            print(f"   🖼️  {Colors.CYAN}PNG:{Colors.END} {png_count} file(s)")
        
        # Move files with error handling
        moved_count = 0
        failed_files = []
        successful_files = []
        
        if RICH_AVAILABLE:
            with Progress() as progress:
                task = progress.add_task("[cyan]Moving files...", total=len(image_files))
                for file in image_files:
                    source_path = os.path.join(source_folder, file)
                    destination_path = os.path.join(destination_folder, file)
                    
                    success, result = safe_file_move(source_path, destination_path, file)
                    
                    if success:
                        moved_count += 1
                        successful_files.append(file)
                    else:
                        failed_files.append((file, result))
                    
                    progress.update(task, advance=1)
        else:
            print(f"\n{Colors.CYAN}Moving files:{Colors.END}")
            for i, file in enumerate(image_files, 1):
                source_path = os.path.join(source_folder, file)
                destination_path = os.path.join(destination_folder, file)
                
                success, result = safe_file_move(source_path, destination_path, file)
                
                if success:
                    moved_count += 1
                    successful_files.append(file)
                    emoji = "🖼️" if file.lower().endswith('.png') else "📷"
                    print(f"   ✅ {emoji} Moved: {file}")
                else:
                    failed_files.append((file, result))
                    print(f"   ❌ Failed: {file}")
        
        # Display results
        if RICH_AVAILABLE:
            if moved_count > 0:
                success_panel = Panel.fit(
                    f"[bold green]🎉 PARTIAL SUCCESS![/]\n\n"
                    f"Moved [cyan]{moved_count}[/] out of [cyan]{len(image_files)}[/] file(s) to:\n"
                    f"[yellow]{destination_folder}[/]\n\n"
                    f"[dim]File breakdown:[/]\n"
                    f"📷 JPG/JPEG files: [cyan]{jpg_count}[/]\n"
                    f"🖼️  PNG files: [cyan]{png_count}[/]",
                    border_style="green",
                    padding=(1, 2)
                )
                console.print(success_panel)
            
            if failed_files:
                error_panel = Panel.fit(
                    f"[bold red]⚠️  FAILED TO MOVE {len(failed_files)} FILE(S)[/]\n\n" +
                    "\n".join([f"[yellow]• {file}:[/] [red]{error}[/]" for file, error in failed_files[:5]]) +
                    (f"\n[dim]... and {len(failed_files) - 5} more[/]" if len(failed_files) > 5 else ""),
                    border_style="red",
                    padding=(1, 2)
                )
                console.print(error_panel)
                
                # Show troubleshooting tips
                if any("cloud" in str(error).lower() for _, error in failed_files):
                    console.print(Panel.fit(
                        "[bold yellow]💡 TROUBLESHOOTING TIPS[/]\n\n"
                        "For 'Cloud File Provider' errors:\n"
                        "1. Check if OneDrive is running properly\n"
                        "2. Try moving files from a different folder\n"
                        "3. Restart OneDrive or your computer\n"
                        "4. Try copying instead of moving files",
                        border_style="yellow"
                    ))
        else:
            if moved_count > 0:
                print(f"\n{Colors.GREEN}{'🎉 PARTIAL SUCCESS!':^60}{Colors.END}")
                print(f"{Colors.GREEN}{'-'*60}{Colors.END}")
                print(f"Moved {Colors.CYAN}{moved_count}{Colors.END} out of {Colors.CYAN}{len(image_files)}{Colors.END} file(s) to:")
                print(f"{Colors.YELLOW}{destination_folder}{Colors.END}")
                print(f"\n{Colors.DIM}File breakdown:{Colors.END}")
                print(f"📷 JPG/JPEG files: {Colors.CYAN}{jpg_count}{Colors.END}")
                print(f"🖼️  PNG files: {Colors.CYAN}{png_count}{Colors.END}")
                print(f"{Colors.GREEN}{'-'*60}{Colors.END}")
            
            if failed_files:
                print(f"\n{Colors.RED}{f'⚠️  FAILED TO MOVE {len(failed_files)} FILE(S)':^60}{Colors.END}")
                for i, (file, error) in enumerate(failed_files[:5], 1):
                    print(f"{Colors.YELLOW}• {file}:{Colors.END} {Colors.RED}{error}{Colors.END}")
                if len(failed_files) > 5:
                    print(f"{Colors.DIM}... and {len(failed_files) - 5} more{Colors.END}")
                
                # Show troubleshooting tips
                if any("cloud" in str(error).lower() for _, error in failed_files):
                    print(f"\n{Colors.YELLOW}{'💡 TROUBLESHOOTING TIPS':^60}{Colors.END}")
                    print(f"{Colors.YELLOW}{'-'*60}{Colors.END}")
                    print(f"{Colors.CYAN}For 'Cloud File Provider' errors:{Colors.END}")
                    print(f"  1. Check if OneDrive is running properly")
                    print(f"  2. Try moving files from a different folder")
                    print(f"  3. Restart OneDrive or your computer")
                    print(f"  4. Try copying instead of moving files")
                    print(f"{Colors.YELLOW}{'-'*60}{Colors.END}")
        
    except Exception as e:
        print_colored(f"\n❌ Error: {str(e)}", Colors.RED)
    
    input("\nPress Enter to continue...")

# ==================== TASK 2: Extract Email Addresses ====================
def task2_extract_emails():
    """Task 2: Extract email addresses with attractive interface"""
    print_header()
    
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold blue]📧 TASK 2: EXTRACT EMAIL ADDRESSES[/]\n"
            "[dim]Extract and organize email addresses from text files[/]",
            border_style="blue"
        ))
        console.print()
    else:
        print(f"{Colors.BLUE}{'TASK 2: EXTRACT EMAIL ADDRESSES':^60}{Colors.END}")
        print(f"{Colors.BLUE}{'-'*60}{Colors.END}\n")
    
    # Get input file
    input_file = Prompt.ask(
        "[cyan]📄 Enter input text file path[/]",
        default="sample_emails.txt"
    ) if RICH_AVAILABLE else input(f"{Colors.CYAN}📄 Enter input text file path (Enter for sample):{Colors.END} ").strip() or "sample_emails.txt"
    
    # Expand user directory shortcuts
    input_file = os.path.expanduser(input_file)
    
    # Create sample file if it doesn't exist
    if not os.path.exists(input_file) and input_file == "sample_emails.txt":
        if RICH_AVAILABLE:
            console.print("[yellow]📝 Creating sample file...[/]")
        else:
            print(f"{Colors.YELLOW}📝 Creating sample file...{Colors.END}")
        
        sample_content = """Sample Email Addresses:
support@example.com
john.doe@company.org
jane_smith123@gmail.com
contact_us@domain.co.uk
sales-department@business.com
info@test-domain.net

Contact us at: help@support.com or call 123-456-7890.
For inquiries: admin@organization.edu, webmaster@site.io

Multiple duplicates: support@example.com, john.doe@company.org"""
        
        try:
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(sample_content)
            print_colored("✅ Sample file created successfully!", Colors.GREEN)
        except Exception as e:
            print_colored(f"❌ Could not create sample file: {str(e)}", Colors.RED)
            input("\nPress Enter to continue...")
            return
    
    if not os.path.exists(input_file):
        print_colored(f"\n❌ Error: File '{input_file}' does not exist!", Colors.RED)
        input("\nPress Enter to continue...")
        return
    
    # Get output file
    output_file = Prompt.ask(
        "[cyan]💾 Enter output file path[/]",
        default="extracted_emails.txt"
    ) if RICH_AVAILABLE else input(f"{Colors.CYAN}💾 Enter output file path (Enter for default):{Colors.END} ").strip() or "extracted_emails.txt"
    
    # Expand user directory shortcuts
    output_file = os.path.expanduser(output_file)
    
    # Extract emails
    try:
        animated_progress("🔍 Extracting email addresses...")
        
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Email regex pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        
        # Remove duplicates while preserving order
        unique_emails = []
        for email in emails:
            email_lower = email.lower()
            if email_lower not in [e.lower() for e in unique_emails]:
                unique_emails.append(email)
        
        if not unique_emails:
            print_colored("\n📭 No email addresses found in the file!", Colors.YELLOW)
            input("\nPress Enter to continue...")
            return
        
        # Save to file
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("=" * 60 + "\n")
            file.write("EXTRACTED EMAIL ADDRESSES\n")
            file.write("=" * 60 + "\n\n")
            file.write(f"Source file: {os.path.basename(input_file)}\n")
            file.write(f"Extraction date: {timestamp}\n")
            file.write(f"Total unique emails: {len(unique_emails)}\n")
            file.write("-" * 60 + "\n\n")
            
            for i, email in enumerate(unique_emails, 1):
                file.write(f"{i:3}. {email}\n")
        
        # Display results
        if RICH_AVAILABLE:
            # Create a panel for results
            domains = {}
            for email in unique_emails:
                domain = email.split('@')[1] if '@' in email else 'Unknown'
                if domain not in domains:
                    domains[domain] = 0
                domains[domain] += 1
            
            domain_list = "\n".join([f"  • {domain}: {count}" for domain, count in sorted(domains.items())])
            
            result_panel = Panel.fit(
                f"[bold green] EXTRACTION COMPLETE![/]\n\n"
                f"[cyan] Statistics:[/]\n"
                f"   Total emails found: {len(emails)}\n"
                f"   Unique emails: {len(unique_emails)}\n"
                f"  Saved to: {output_file}\n\n"
                f"[cyan] Domain Breakdown:[/]\n{domain_list}",
                border_style="green",
                padding=(1, 2)
            )
            console.print(result_panel)
            
            # Show sample emails
            if len(unique_emails) > 0:
                console.print(f"\n[cyan]📨 Sample Emails:[/]")
                for i, email in enumerate(unique_emails[:5], 1):
                    console.print(f"  {i}. {email}")
                if len(unique_emails) > 5:
                    console.print(f"  ... and [cyan]{len(unique_emails) - 5}[/] more")
        else:
            print(f"\n{Colors.GREEN} EXTRACTION COMPLETE!{Colors.END}")
            print(f"\n{Colors.CYAN}Statistics:{Colors.END}")
            print(f"   Total emails found: {len(emails)}")
            print(f"   Unique emails: {len(unique_emails)}")
            print(f"   Saved to: {output_file}")
            
            if len(unique_emails) > 0:
                print(f"\n{Colors.CYAN}📨 Sample Emails:{Colors.END}")
                for i, email in enumerate(unique_emails[:5], 1):
                    print(f"  {i}. {email}")
                if len(unique_emails) > 5:
                    print(f"  ... and {len(unique_emails) - 5} more")
        
    except Exception as e:
        print_colored(f"\nError: {str(e)}", Colors.RED)
    
    input("\nPress Enter to continue...")

# ==================== TASK 3: Scrape Webpage Title ====================
def task3_scrape_webpage():
    """Task 3: Scrape webpage title with attractive interface"""
    print_header()
    
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold magenta]🌐 TASK 3: SCRAPE WEBPAGE TITLE[/]\n"
            "[dim]Extract information from web pages[/]",
            border_style="magenta"
        ))
        console.print()
    else:
        print(f"{Colors.MAGENTA}{'TASK 3: SCRAPE WEBPAGE TITLE':^60}{Colors.END}")
        print(f"{Colors.MAGENTA}{'-'*60}{Colors.END}\n")
    
    # Check if BeautifulSoup is available
    try:
        from bs4 import BeautifulSoup
        bs4_available = True
    except ImportError:
        if RICH_AVAILABLE:
            console.print("[red] Missing Dependencies[/]")
            console.print("[yellow]BeautifulSoup4 is not installed.[/]")
            console.print("\n Install with: [cyan]pip install beautifulsoup4[/]")
        else:
            print(f"{Colors.RED} Missing Dependencies{Colors.END}")
            print(f"{Colors.YELLOW}BeautifulSoup4 is not installed.{Colors.END}")
            print(f"\n Install with: {Colors.CYAN}pip install beautifulsoup4{Colors.END}")
        input("\nPress Enter to continue...")
        return
    
    # URL selection
    test_urls = {
        "1": (" Example.com", "https://example.com/"),
        "2": (" Wikipedia", "https://en.wikipedia.org/wiki/Web_scraping"),
        "3": (" Google", "https://www.google.com/"),
        "4": (" Fast Test", "https://httpbin.org/html"),
        "5": (" Custom URL", "custom")
    }
    
    if RICH_AVAILABLE:
        console.print("[cyan]Select a URL to scrape:[/]")
        for key, (name, url) in test_urls.items():
            if key == "5":
                console.print(f"  [bold]{key}.[/] {name}")
            else:
                console.print(f"  [bold]{key}.[/] {name} [dim]({url})[/]")
    else:
        print(f"{Colors.CYAN} Select a URL to scrape:{Colors.END}")
        for key, (name, url) in test_urls.items():
            if key == "5":
                print(f"  {key}. {name}")
            else:
                print(f"  {key}. {name} ({url})")
    
    choice = Prompt.ask("\n[cyan]Enter choice[/]", choices=["1", "2", "3", "4", "5"], default="1") if RICH_AVAILABLE else input(f"\n{Colors.CYAN}Enter choice (1-5):{Colors.END} ").strip() or "1"
    
    if choice == "5":
        url = Prompt.ask("[cyan]Enter custom URL[/]", default="https://example.com") if RICH_AVAILABLE else input(f"{Colors.CYAN}Enter custom URL:{Colors.END} ").strip() or "https://example.com"
    else:
        url = test_urls[choice][1]
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Scrape the webpage
    if RICH_AVAILABLE:
        console.print(f"\n[cyan] Connecting to:[/] [yellow]{url}[/]")
    else:
        print(f"\n{Colors.CYAN} Connecting to:{Colors.END} {Colors.YELLOW}{url}{Colors.END}")
    
    try:
        animated_progress(" Fetching webpage...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract information
        title_tag = soup.find('title')
        title = title_tag.string.strip() if title_tag else "No title found"
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'] if meta_desc else "No description found"
        
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords = meta_keywords['content'] if meta_keywords else "No keywords found"
        
        # Generate output filename
        domain = url.split('//')[-1].split('/')[0].replace('www.', '')
        safe_domain = "".join(c for c in domain if c.isalnum() or c in ('-', '_'))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"webpage_{safe_domain}_{timestamp}.txt"
        
        # Save to file
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output_content = f"""WEBPAGE INFORMATION SCRAPER
{'='*60}

URL: {url}
Scraped at: {timestamp_str}
Status: {response.status_code} {response.reason}

{'='*60}

 PAGE TITLE:
{title}

{'='*60}

 META DESCRIPTION:
{description}

{'='*60}

  META KEYWORDS:
{keywords}

{'='*60}

🔧 TECHNICAL DETAILS:
- Content Type: {response.headers.get('content-type', 'Unknown')}
- Content Length: {len(response.content):,} bytes
- Encoding: {response.encoding}
- Server: {response.headers.get('server', 'Unknown')}

{'='*60}"""
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(output_content)
        
        # Display results
        if RICH_AVAILABLE:
            success_panel = Panel.fit(
                f"[bold green] WEBPAGE SCRAPED SUCCESSFULLY![/]\n\n"
                f"[cyan] Page Information:[/]\n"
                f"  Title: {title[:50]}{'...' if len(title) > 50 else ''}\n"
                f"   Description: {description[:50]}{'...' if len(description) > 50 else ''}\n"
                f"   URL: {url}\n"
                f"   Saved to: {output_file}\n\n"
                f"[cyan]  Technical Details:[/]\n"
                f"   Status: {response.status_code}\n"
                f"   Size: {len(response.content):,} bytes\n"
                f"   Time: {timestamp_str}",
                border_style="green",
                padding=(1, 2)
            )
            console.print(success_panel)
            
            # Show title in a nice box
            title_panel = Panel.fit(
                f"[bold cyan]{title}[/]",
                title="[yellow]Page Title[/]",
                border_style="cyan"
            )
            console.print(f"\n{title_panel}")
            
        else:
            print(f"\n{Colors.GREEN} WEBPAGE SCRAPED SUCCESSFULLY!{Colors.END}")
            print(f"\n{Colors.CYAN}Page Information:{Colors.END}")
            print(f"   Title: {title[:50]}{'...' if len(title) > 50 else ''}")
            print(f"   Description: {description[:50]}{'...' if len(description) > 50 else ''}")
            print(f"  URL: {url}")
            print(f"   Saved to: {output_file}")
            print(f"\n{Colors.CYAN}⚙️  Technical Details:{Colors.END}")
            print(f"   Status: {response.status_code}")
            print(f"   Size: {len(response.content):,} bytes")
            print(f"  Time: {timestamp_str}")
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error {e.response.status_code}: {e.response.reason}"
        print_colored(f"\n {error_msg}", Colors.RED)
    except requests.exceptions.ConnectionError:
        print_colored("\nConnection Error: Could not connect to the server", Colors.RED)
    except requests.exceptions.Timeout:
        print_colored("\n Timeout Error: The request took too long", Colors.RED)
    except Exception as e:
        print_colored(f"\n Error: {str(e)}", Colors.RED)
    
    input("\nPress Enter to continue...")

# ==================== MAIN PROGRAM ====================
def main():
    """Main program loop with attractive interface"""
    
    # Check for rich installation
    if not RICH_AVAILABLE:
        print_colored("\n Tip: Install 'rich' for better visuals:", Colors.YELLOW)
        print_colored("   pip install rich\n", Colors.CYAN)
        sleep(2)
    
    while True:
        print_menu()
        
        try:
            if RICH_AVAILABLE:
                choice = Prompt.ask(
                    "[bold cyan]Enter your choice[/]",
                    choices=["1", "2", "3", "4", "help"],
                    default="1"
                )
            else:
                choice = input(f"\n{Colors.CYAN}Enter your choice (1-4):{Colors.END} ").strip()
            
            if choice == "1":
                task1_move_image_files()
            elif choice == "2":
                task2_extract_emails()
            elif choice == "3":
                task3_scrape_webpage()
            elif choice == "4":
                print_header()
                farewell_messages = [
                    " Thank you for using Task Automation Script! ",
                    " Hope it made your tasks easier! ",
                    " Goodbye and have a great day! ",
                    " Keep automating! See you next time! "
                ]
                msg = random.choice(farewell_messages)
                print_colored(msg, Colors.CYAN)
                print()
                break
            elif choice.lower() == "help":
                print_header()
                print_colored(" Help & Instructions", Colors.CYAN)
                print_colored("-" * 40, Colors.CYAN)
                print("\nThis script helps you automate three common tasks:")
                print("1.  Move image files (JPG, PNG) between folders")
                print("2. Extract email addresses from text files")
                print("3.  Scrape webpage titles and information")
                print("\n Tips:")
                print("   • Use Enter to accept defaults")
                print("   • Install 'rich' for better visuals")
                print("   • For Task 3, install: pip install beautifulsoup4")
                print("   • For Task 1: Avoid OneDrive folders if you get cloud errors")
                input("\nPress Enter to continue...")
            else:
                print_colored(" Invalid choice! Please enter 1, 2, 3, or 4.", Colors.RED)
                sleep(1)
                
        except KeyboardInterrupt:
            print_colored("\n\n Operation cancelled by user.", Colors.YELLOW)
            if RICH_AVAILABLE:
                confirm = Confirm.ask("Exit program?")
            else:
                confirm = input(f"{Colors.YELLOW}Exit program? (y/n):{Colors.END} ").lower() == 'y'
            
            if confirm:
                print_colored("\n Goodbye!", Colors.CYAN)
                break
        except Exception as e:
            print_colored(f"\n An unexpected error occurred: {str(e)}", Colors.RED)
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 6):
        print_colored(" This script requires Python 3.6 or higher!", Colors.RED)
        sys.exit(1)
    
    # Installation instructions
    print_header()
    if not RICH_AVAILABLE:
        print_colored(" Task Automation Script - Enhanced Version ", Colors.CYAN)
        print_colored("=" * 50, Colors.CYAN)
        print("\n For the best experience, install optional packages:")
        print_colored("   pip install rich requests beautifulsoup4", Colors.YELLOW)
        print("\n  For Task 1: Avoid OneDrive/synced folders if you get cloud errors")
        print("\nPress Enter to continue...")
        input()
    
    # Run the main program
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n Goodbye!", Colors.CYAN)
    except Exception as e:
        print_colored(f"\n Fatal error: {str(e)}", Colors.RED)
        input("Press Enter to exit...")