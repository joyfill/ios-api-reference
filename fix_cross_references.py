#!/usr/bin/env python3
"""
Script to fix cross-module documentation references in DocC static sites.
Adds missing cross-module references from Joyfill to JoyfillModel/JoyfillFormulas/JoyfillAPIService.
"""

import json
import os
import sys
from pathlib import Path

def fix_cross_module_references(docs_path):
    """Fix cross-module references by adding missing reference entries."""
    
    # Define cross-module types and their target modules
    cross_module_types = {
        'JoyDoc': {
            'module': 'JoyfillModel',
            'identifier': 's:12JoyfillModel6JoyDocV',
            'url': '/documentation/joyfillmodel/joydoc',
            'kind': 'symbol',
            'role': 'symbol',
            'title': 'JoyDoc',
            'fragments': [
                {'kind': 'keyword', 'text': 'struct'},
                {'kind': 'text', 'text': ' '},
                {'kind': 'identifier', 'text': 'JoyDoc'}
            ],
            'abstract': [{'type': 'text', 'text': 'The main document model for Joyfill forms.'}],
            'type': 'topic'
        },
        'JoyDocField': {
            'module': 'JoyfillModel',
            'identifier': 's:12JoyfillModel11JoyDocFieldC',
            'url': '/documentation/joyfillmodel/joydocfield',
            'kind': 'symbol',
            'role': 'symbol',
            'title': 'JoyDocField',
            'fragments': [
                {'kind': 'keyword', 'text': 'class'},
                {'kind': 'text', 'text': ' '},
                {'kind': 'identifier', 'text': 'JoyDocField'}
            ],
            'abstract': [{'type': 'text', 'text': 'Represents a field in a Joyfill document.'}],
            'type': 'topic'
        },
        'ValueUnion': {
            'module': 'JoyfillModel',
            'identifier': 's:12JoyfillModel10ValueUnionO',
            'url': '/documentation/joyfillmodel/valueunion',
            'kind': 'symbol',
            'role': 'symbol',
            'title': 'ValueUnion',
            'fragments': [
                {'kind': 'keyword', 'text': 'enum'},
                {'kind': 'text', 'text': ' '},
                {'kind': 'identifier', 'text': 'ValueUnion'}
            ],
            'abstract': [{'type': 'text', 'text': 'A union type representing different value types in Joyfill fields.'}],
            'type': 'topic'
        },
        'ChangeEvent': {
            'module': 'JoyfillModel',
            'identifier': 's:12JoyfillModel11ChangeEventV',
            'url': '/documentation/joyfillmodel/changeevent',
            'kind': 'symbol',
            'role': 'symbol',
            'title': 'ChangeEvent',
            'fragments': [
                {'kind': 'keyword', 'text': 'struct'},
                {'kind': 'text', 'text': ' '},
                {'kind': 'identifier', 'text': 'ChangeEvent'}
            ],
            'abstract': [{'type': 'text', 'text': 'Represents a change event in the document.'}],
            'type': 'topic'
        },
    }
    
    joyfill_data_dir = Path(docs_path) / 'Joyfill' / 'data' / 'documentation' / 'joyfill'
    
    if not joyfill_data_dir.exists():
        print(f"Error: {joyfill_data_dir} does not exist")
        return
    
    files_updated = 0
    references_added = 0
    
    # Walk through all JSON files in the Joyfill documentation
    for json_file in joyfill_data_dir.rglob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'references' not in data:
                continue
            
            file_modified = False
            file_content = json.dumps(data, ensure_ascii=False)
            
            # Check which cross-module types are mentioned in this file
            for type_name, type_info in cross_module_types.items():
                precise_id = type_info['identifier']
                ref_key = f"doc://components-swift.{type_info['module']}/documentation/{type_info['module']}/{type_name}"
                
                # Check if the type is referenced but not in the references section
                if precise_id in file_content and ref_key not in data['references']:
                    # Add the missing reference
                    data['references'][ref_key] = {
                        'identifier': ref_key,
                        'url': type_info['url'],
                        'kind': type_info['kind'],
                        'role': type_info['role'],
                        'title': type_info['title'],
                        'fragments': type_info['fragments'],
                        'abstract': type_info['abstract'],
                        'type': type_info['type']
                    }
                    
                    file_modified = True
                    references_added += 1
                    print(f"Added {type_name} reference to {json_file.relative_to(docs_path)}")
            
            # Save the modified file
            if file_modified:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
                files_updated += 1
        
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    print(f"\nSummary:")
    print(f"  Files updated: {files_updated}")
    print(f"  Cross-module references added: {references_added}")

if __name__ == '__main__':
    docs_path = Path(__file__).parent / 'docs'
    if len(sys.argv) > 1:
        docs_path = Path(sys.argv[1])
    
    print(f"Fixing cross-module references in: {docs_path}")
    fix_cross_module_references(docs_path)
    print("Done!")

