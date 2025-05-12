#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 13:07:23 2025

@author: juda
"""

import os
import logging
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from marker.converters.pdf import PdfConverter

    
def convert_pdf(pdf_path, output_dir, gemini_api_key):
    """
    Convert a PDF file to markdown using Marker's PdfConverter.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_dir (str): Directory where the output markdown file will be saved
        gemini_api_key (str): API key for Gemini LLM service
        
    Returns:
        str: Path to the output markdown file, or None if processing failed
    """
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_md_path = os.path.join(output_dir, f"{base_name}_PdfConverter_output.md")
    
    # If output file already exists, return its path without processing again
    if os.path.exists(output_md_path):
        logging.info(f"Output file already exists: {output_md_path}")
        return output_md_path
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        # Define the Marker Configuration
        marker_config_dict = {
            "output_format": "markdown",
            "languages": 'en',
            "disable_image_extraction": True,
            "use_llm": True,
            "gemini_api_key": gemini_api_key,
            #"model_name": "",    
        }
        
        logging.info(f"Initializing ConfigParser with config: {marker_config_dict}")
        config_parser = ConfigParser(marker_config_dict)
        
        # Generate the specific configurations for the PdfConverter
        converter_internal_config = config_parser.generate_config_dict()
        processor_list = config_parser.get_processors()
        renderer = config_parser.get_renderer() 
        llm_service = config_parser.get_llm_service() 
        
        logging.info("Initializing PdfConverter...")
        converter = PdfConverter(
            config=converter_internal_config,
            artifact_dict=create_model_dict(), 
            processor_list=processor_list,
            renderer=renderer,
            llm_service=llm_service
        )
        
        logging.info(f"Converting PDF: {pdf_path} using PdfConverter...")
        # The converter instance is callable with the file path
        rendered_output = converter(pdf_path)
        
        # Output Handling
        if rendered_output:
            final_markdown = rendered_output.markdown # Assuming rendered_output is the Markdown string
            
            
            with open(output_md_path, "w", encoding="utf-8") as f:
                f.write(final_markdown)
                
            logging.info(f"Successfully processed PDF with PdfConverter. Output saved to: {output_md_path}")
            return output_md_path
        else:
            logging.error(f"PdfConverter processing failed for {pdf_path}. No output generated.")
            return None
            
    except ImportError as e:
        logging.error(f"ImportError encountered: {e}")
        logging.error("Please ensure 'marker-pdf' and its dependencies are installed correctly and class paths are valid.")
        return None
    except AttributeError as e:
        logging.error(f"AttributeError: {e}. This might indicate an incorrect method call or that ConfigParser/PdfConverter doesn't have an expected method.")
        logging.error("Double-check the methods like 'generate_config_dict', 'get_processors', etc., against Marker's actual API.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        return None
    

def main():
    """
    Main function to handle command line arguments and execute the PDF conversion.
    """
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Convert PDF to markdown using Marker library')
    
    # Add arguments
    parser.add_argument('--pdf_path', type=str, required=True, 
                        help='Path to the input PDF file')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Directory where the output markdown file will be saved')
    parser.add_argument('--api_key', type=str, 
                        default=os.environ.get('GEMINI_API_KEY', ''), 
                        help='API key for Gemini LLM service')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the conversion
    output_path = convert_pdf(args.pdf_path, args.output_dir, args.api_key)
    
    # Print results
    if output_path:
        print(f"PDF successfully converted. Output file: {output_path}")
    else:
        print("PDF conversion failed. Check logs for details.")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())