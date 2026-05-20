# Ghost Apply Enhancements

## From Sharbel's List - What We Can Integrate

### 1. Resume PDF Generation (resume-cli)
```bash
npm install -g resume-cli
resume export resume.pdf --format pdf --theme elegant
```

**Use Case:**
- Convert profile.json → Professional PDF
- Multiple themes (elegant, flat, class, etc.)
- ATS-friendly formats

**Integration:**
```python
# After optimization, generate PDF
subprocess.run(['resume', 'export', 'tailored_resume.pdf', '--theme', 'elegant'])
```

### 2. Web Dashboard (Reactive-Resume)
```bash
docker run -p 3000:3000 amruthpillai/reactive-resume:latest
```

**Use Case:**
- Visual profile editor
- Template selection
- Export to Ghost Apply

**Integration:**
- iframe in dashboard
- Import/Export profile.json

### 3. Template System (best-resume-ever)
```bash
git clone https://github.com/salomonelli/best-resume-ever.git
cd best-resume-ever
npm install
npm run export
```

**Use Case:**
- Multiple resume designs
- Material, SideBar, LeftRight templates
- PDF export

**Integration:**
- Add as git submodule
- Script to fill templates from profile.json

## Implementation Priority

### Phase 1: Resume PDF Export
- [ ] Install resume-cli globally
- [ ] Create wrapper script
- [ ] Add to optimizer workflow
- [ ] Test with profile.json

### Phase 2: Template System
- [ ] Clone best-resume-ever
- [ ] Map profile.json to template variables
- [ ] Add template selection to optimizer
- [ ] Generate multiple versions

### Phase 3: Web Dashboard (Future)
- [ ] Set up Reactive-Resume locally
- [ ] Create profile.json import/export
- [ ] Integration with Ghost Apply

## Quick Win

Add to `smart_optimizer.py`:
```python
def generate_pdf_resume(self, theme='elegant'):
    """Generate PDF using resume-cli"""
    import subprocess
    import json
    
    # Convert profile to JSON Resume format
    resume_json = self._convert_to_json_resume()
    
    # Save temporary file
    with open('/tmp/resume.json', 'w') as f:
        json.dump(resume_json, f)
    
    # Generate PDF
    subprocess.run([
        'resume', 'export', 
        f'/tmp/tailored_resume_{theme}.pdf',
        '--format', 'pdf',
        '--theme', theme
    ])
    
    return f'/tmp/tailored_resume_{theme}.pdf'
```

## Benefits

- Professional PDF output
- Multiple design options
- ATS-friendly formats
- Industry standard (JSON Resume)
- Free (open source)

## Action Item

Install resume-cli now:
```bash
npm install -g resume-cli
```

Then enhance optimizer to generate PDFs automatically.
