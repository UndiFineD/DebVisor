# DebVisor Web Panel - Input Validation & Output Escaping Guide

This document provides comprehensive guidance on input validation, output escaping, and XSS prevention for the DebVisor web panel.

## Table of Contents

1. Overview

1. Input Validation Strategy

1. Output Escaping & XSS Prevention

1. Validation Patterns

1. Context-Specific Escaping

1. Common Vulnerabilities

1. Implementation Checklist

## Overview

### The Problem

Web applications receive user input from many sources:

- Form submissions

- URL parameters

- API requests

- Cookies

- Headers

### Malicious input can cause

- **SQL Injection**: Execute arbitrary database queries

- **Command Injection**: Execute arbitrary system commands

- **Cross-Site Scripting (XSS)**: Execute arbitrary JavaScript in other users' browsers

- **Path Traversal**: Access files outside intended directory

- **Buffer Overflow**: Crash application or execute code

### The Solution

### Defense in Depth

1.**Input Validation**: Accept only known-good data
1.**Output Escaping**: Render data safely for each context
1.**Security Headers**: Control what browsers can do
1.**Content Security Policy**: Restrict script execution

## Input Validation Strategy

### Whitelist vs Blacklist

- *? Don't use blacklist**(block specific bad things):

## BAD: Try to block specific dangerous characters

    def is_safe(input_str):
        dangerous = ['', '"', "'", ';', '--']
        for char in dangerous:
            if char in input_str:
                return False
        return True

## Attacker bypasses: <%65%6E%63%6F%64%65%64 attacks

- *? Use whitelist**(accept only known-good things):

## GOOD: Accept only RFC-compliant hostnames

    def validate_hostname(hostname):
        if not hostname or len(hostname) > 253:
            return False

## RFC 1123: labels are 1-63 chars, alphanumeric and hyphen

        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        return bool(re.match(pattern, hostname))

## Only: "node-01", "node.01" pass; "" fails

## Validation Levels

### Level 1: Type Checking

## Validate input type

    def level1_type_check(value, expected_type):
        """Reject wrong types"""
        if not isinstance(value, expected_type):
            raise ValidationError(f'Expected {expected_type.**name**}')
        return value

## Usage

    pool_name = request.form.get('pool')
    pool_name = level1_type_check(pool_name, str)  # Ensure string

## Level 2: Format Validation

    import re
    def level2_format_check(value, pattern):
        """Validate against regex pattern"""
        if not re.match(pattern, value):
            raise ValidationError('Invalid format')
        return value

## Usage [2]

    hostname = request.form.get('hostname')
    hostname = level2_format_check(hostname, r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$')

## Level 3: Length Validation

    def level3_length_check(value, min_len=1, max_len=1000):
        """Validate string length"""
        if len(value)  max_len:
            raise ValidationError(f'Length must be {min_len}-{max_len}')
        return value

## Usage [3]

    hostname = level3_length_check(hostname, min_len=1, max_len=253)

## Level 4: Range Validation

    def level4_range_check(value, min_val=None, max_val=None):
        """Validate numeric range"""
        value = int(value)
        if min_val is not None and value < min_val:
            raise ValidationError(f'Value must be >= {min_val}')
        if max_val is not None and value > max_val:
            raise ValidationError(f'Value must be <= {max_val}')
        return value

## Usage [4]

    port = level4_range_check(request.form.get('port'), min_val=1024, max_val=65535)

## Level 5: Business Logic Validation

    def level5_business_logic(hostname, user_role):
        """Validate against business rules"""

## User can only modify nodes in their environment

        node = Node.query.filter_by(hostname=hostname).first()
        if not node:
            raise ValidationError('Node not found')
        if user_role == 'developer' and node.environment == 'production':
            raise ValidationError('Developers cannot modify production nodes')
        return node

## Usage [5]

    node = level5_business_logic(hostname, current_user.role)

## Output Escaping & XSS Prevention

### Context Matters

### Same data, different contexts

    {{ user_name }}
      var name = "{{ user_name }}";
      .user { color: {{ user_color }}; }
    Search
Each context requires**different escaping**.

### HTML Escaping

    from markupsafe import escape

## HTML escaping converts special chars to entities

    def html_escape(text):
        """Escape for HTML content context"""
        return escape(text)

## Example

    user_input = 'alert("XSS")'
    escaped = html_escape(user_input)

## Result: &lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt

## In Jinja2 templates (automatic)

    {% raw %}
    Welcome {{ username }}
    {% endraw %}

## HTML Attribute Escaping

    def html_attr_escape(text):
        """Escape for HTML attribute context"""
        text = escape(text)

## Additional escaping for attributes

        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#x27;')
        return text

## Example [2]

    user_input = 'test" onload="alert(1)'
    escaped = html_attr_escape(user_input)

## Result: test&quot; onload=&quot;alert(1)

## In template attribute

    {% raw %}
    {% endraw %}

## JavaScript String Escaping

    import json
    def js_string_escape(text):
        """Escape for JavaScript string literal context"""

## Use json.dumps which handles all escaping

        return json.dumps(text)

## Example [3]

    user_input = 'test"; alert("XSS'
    escaped = js_string_escape(user_input)

## Result: "test\"; alert(\"XSS"

## Usage in template

    {% raw %}
      var username = {{ username | tojson }};
    {% endraw %}

## CSS Escaping

    import re
    def css_escape(text):
        """Escape for CSS context"""

## Remove all special CSS characters

## CSS identifiers: alphanumeric, hyphen, underscore, non-ASCII, escaped chars

## For safety, only allow safe subset

        safe_chars = re.sub(r'[^a-zA-Z0-9_-]', '', text)
        return safe_chars

## Example [4]

    user_input = 'red; background: url(javascript:alert(1))'
    escaped = css_escape(user_input)

## Result: red-backgroundurljava?scriptalert1

## For colors specifically

    def css_color_escape(color):
        """Validate and escape CSS color"""

## Only allow hex colors #RRGGBB or named colors

        if re.match(r'^#[0-9a-fA-F]{6}$', color):
            return color
        if color in ['red', 'blue', 'green', 'black', 'white']:
            return color
        raise ValueError('Invalid color')

## URL Escaping

    from urllib.parse import quote
    def url_param_escape(text):
        """Escape for URL parameter context"""

## URL encode special characters

        return quote(text, safe='')

## Example [5]

    user_input = 'hello world&param=value'
    escaped = url_param_escape(user_input)

## Result: hello%20world%26param%3Dvalue

## In template

    {% raw %}
    Search
    {% endraw %}

## Validation Patterns

### Common Data Types

    import re
    from ipaddress import IPv4Address, IPv6Address, ip_address
    class Validators:
        """Reusable validation patterns"""

## Network identifiers

        @staticmethod
        def validate_hostname(value):
            """RFC 1123 hostname"""
            pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
            if not re.match(pattern, value):
                raise ValueError('Invalid hostname')
            if len(value) > 253:
                raise ValueError('Hostname too long')
            return value
        @staticmethod
        def validate_ipv4(value):
            """IPv4 address"""
            try:
                ip = IPv4Address(value)
                return str(ip)
            except Exception:
                raise ValueError('Invalid IPv4 address')
        @staticmethod
        def validate_ipv6(value):
            """IPv6 address"""
            try:
                ip = IPv6Address(value)
                return str(ip)
            except Exception:
                raise ValueError('Invalid IPv6 address')
        @staticmethod
        def validate_mac_address(value):
            """MAC address (XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX)"""
            pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
            if not re.match(pattern, value):
                raise ValueError('Invalid MAC address')
            return value.upper()
        @staticmethod
        def validate_port(value):
            """TCP/UDP port (1-65535)"""
            port = int(value)
            if port  65535:
                raise ValueError('Port out of range (1-65535)')
            return port

## Identifiers

        @staticmethod
        def validate_uuid(value):
            """UUID (RFC 4122)"""
            pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            if not re.match(pattern, value, re.IGNORECASE):
                raise ValueError('Invalid UUID')
            return value.lower()
        @staticmethod
        def validate_pool_name(value):
            """Storage pool name"""
            pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_-]{0,30}[a-zA-Z0-9]$'
            if not re.match(pattern, value):
                raise ValueError('Invalid pool name (alphanumeric, hyphen, underscore only)')
            return value
        @staticmethod
        def validate_snapshot_name(value):
            """Snapshot name"""
            pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_-]{0,62}[a-zA-Z0-9]$'
            if not re.match(pattern, value):
                raise ValueError('Invalid snapshot name')
            return value
        @staticmethod
        def validate_vm_name(value):
            """Virtual machine name"""
            pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}[a-zA-Z0-9]$'
            if not re.match(pattern, value):
                raise ValueError('Invalid VM name')
            return value

## Email and text

        @staticmethod
        def validate_email(value):
            """Email address (simplified)"""
            pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
            if not re.match(pattern, value):
                raise ValueError('Invalid email address')
            return value.lower()
        @staticmethod
        def validate_username(value):
            """Linux username (3-32 chars)"""
            pattern = r'^[a-z_][a-z0-9_-]{2,31}$'
            if not re.match(pattern, value):
                raise ValueError('Invalid username (3-32 alphanumeric, underscore, hyphen)')
            return value
        @staticmethod
        def validate_url(value):
            """HTTP/HTTPS URL"""
            pattern = r'^https?://[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*(/[a-zA-Z0-9._~:/?#[\]@!$&\'()*+,;=-]*)?$'
            if not re.match(pattern, value):
                raise ValueError('Invalid URL')
            if len(value) > 2048:
                raise ValueError('URL too long')
            return value
        @staticmethod
        def validate_cidr(value):
            """CIDR notation (192.168.1.0/24)"""
            try:
                from ipaddress import ip_network
                net = ip_network(value, strict=False)
                return str(net)
            except Exception:
                raise ValueError('Invalid CIDR notation')

## Usage [6]

    @app.route('/api/nodes', methods=['POST'])
    @login_required
    def create_node():
        """Create node with validated input"""
        try:
            hostname = Validators.validate_hostname(request.form.get('hostname', ''))
            mgmt_ip = Validators.validate_ipv4(request.form.get('mgmt_ip', ''))
            mac_addr = Validators.validate_mac_address(request.form.get('mac', ''))

## RPC call

            result = rpc_client.create_node(hostname, mgmt_ip, mac_addr)
            audit_log('AUDIT', f'Created node {hostname}')
            return jsonify(result)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

## Context-Specific Escaping

### Complete Flask Application with Escaping

    from flask import Flask, render_template, request, jsonify, escape
    from markupsafe import Markup
    import html
    import json
    app = Flask(**name**)

## Context 1: HTML Template (automatic)

    @app.route('/node/')
    def node_detail(node_id):
        """Node detail page with automatic HTML escaping"""
        node = rpc_client.get_node_info(node_id)

## Jinja2 automatically escapes {{ node.hostname }}

        return render_template('node.html', node=node)

## HTML template

    """
    Node: {{ node.hostname }}
    Status: {{ node.status }}
    Description: {{ node.description }}
    """

## Context 2: HTML Attribute

    @app.route('/search')
    def search():
        """Search with user input in attribute"""
        query = request.args.get('q', '')

## Use urlencode for URL parameters

        return render_template('search.html', query=query)

## HTML template [2]

    """
        Search
    """

## Context 3: JavaScript

    @app.route('/api/dashboard')
    def dashboard_api():
        """Return dashboard data as JSON (safe for JS context)"""
        user_data = {
            'username': current_user.username,
            'role': current_user.role,
            'node_count': len(rpc_client.list_nodes()),
        }
        return jsonify(user_data)

## JavaScript

    """
    fetch('/api/dashboard')
        .then(r => r.json())
        .then(data => {
            document.getElementById('username').textContent = data.username;
        });
    """

## Context 4: CSV Export (special escaping)

    @app.route('/export/nodes.csv')
    @login_required
    def export_nodes_csv():
        """Export nodes as CSV"""
        nodes = rpc_client.list_nodes()
        csv_lines = ['hostname,ip,status,description']
        for node in nodes:

## CSV escaping: quotes and newlines

            def csv_escape(value):
                if '"' in value or ',' in value or '\n' in value:
                    return f'"{value.replace('"', '""')}"'
                return value
            line = ','.join([
                csv_escape(node.hostname),
                csv_escape(node.ip),
                csv_escape(node.status),
                csv_escape(node.description),
            ])
            csv_lines.append(line)
        response = app.make_response('\n'.join(csv_lines))
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=nodes.csv'
        return response

## Context 5: Markdown rendering

    from markupsafe import Markup
    import bleach
    @app.route('/notes/')
    def view_note(note_id):
        """View note with safe markdown rendering"""
        note = Note.query.get(note_id)

## Sanitize markdown content (allow only safe HTML)

        allowed_tags = ['p', 'br', 'strong', 'em', 'code', 'pre', 'blockquote', 'ul', 'ol', 'li']
        allowed_attrs = {}

## First: render markdown to HTML

        import markdown
        html_content = markdown.markdown(note.content)

## Then: sanitize HTML

        clean_html = bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attrs)
        return render_template('note.html', content=Markup(clean_html))

## JSON API Response

    @app.route('/api/nodes//logs')
    def get_node_logs(node_id):
        """Get node logs as JSON"""
        logs = rpc_client.get_node_logs(node_id)

## All data automatically escaped by jsonify

        return jsonify({
            'node_id': node_id,
            'logs': [
                {
                    'timestamp': log.timestamp.isoformat(),
                    'level': log.level,
                    'message': log.message,  # Automatically escaped
                }
                for log in logs
            ]
        })

## Common Vulnerabilities

### XSS Examples

### Vulnerability 1: Direct output without escaping

## ? VULNERABLE

    @app.route('/greeting/')
    def greeting(name):
        return f'Hello {name}'  # name not escaped

## Attack: /greeting/alert('XSS')

## Result: Hello alert('XSS')

## Fix

## ? SAFE

    @app.route('/greeting/')
    def greeting(name):
        return render_template('greeting.html', name=name)

## Or: return f'Hello {escape(name)}'

## Vulnerability 2: User data in JavaScript

## ? VULNERABLE [2]

    {% raw %}
      var username = "{{ username }}";  // Not escaped for JS context
    {% endraw %}

## Attack: username = "; alert('XSS'); var x = "

## Result

## var username = ""; alert('XSS'); var x = ""

## Fix [2]

## ? SAFE [2]

    {% raw %}
      var username = {{ username | tojson }};  // Properly escaped
    {% endraw %}

## Vulnerability 3: User data in HTML attribute

     - ->

### Vulnerability 4: User data in URL

## ? VULNERABLE [3]

    {% raw %}
    Search
    Search -->
    {% endraw %}

## ? SAFE [3]

    {% raw %}
    Search
    {% endraw %}

## SQL Injection Examples

### Vulnerability: String concatenation in SQL

## ? VULNERABLE [4]

    @app.route('/nodes/')
    def get_node(hostname):

## BAD: Directly inserting user input into SQL

        query = f"SELECT * FROM nodes WHERE hostname = '{hostname}'"
        result = db.session.execute(query)
        return result

## Attack: hostname = "'; DROP TABLE nodes; --"

## SQL: SELECT * FROM nodes WHERE hostname = ''; DROP TABLE nodes; --'

## Fix: Parameterized queries

## ? SAFE [4]

    @app.route('/nodes/')
    def get_node(hostname):

## GOOD: Using parameterized queries (ORM)

        result = Node.query.filter_by(hostname=hostname).first()
        return result

## Or with raw SQL

## query = "SELECT * FROM nodes WHERE hostname = ?"

## result = db.session.execute(query, (hostname,))

## Command Injection Examples

### Vulnerability: String concatenation in shell command

## ? VULNERABLE [5]

    import subprocess
    @app.route('/api/nodes//ping')
    def ping_node(node_id):

## BAD: Shell command with user input

        cmd = f"ping -c 4 {node_id}"
        result = subprocess.run(cmd, shell=True, capture_output=True)
        return result.stdout.decode()

## Attack: node_id = "127.0.0.1; rm -rf /"

## Shell: ping -c 4 127.0.0.1; rm -rf /

## Fix: Avoid shell, use argument list

## ? SAFE [5]

    @app.route('/api/nodes//ping')
    def ping_node(node_id):

## Validate hostname first

        hostname = Validators.validate_hostname(node_id)

## Use argument list, no shell

        result = subprocess.run(['ping', '-c', '4', hostname],
                               capture_output=True, text=True, shell=False)
        return result.stdout

## Implementation Checklist

### Input Validation

- [ ] All user input validated (form, query params, API body)

- [ ] Whitelist approach used (accept known-good input)

- [ ] Type checking implemented

- [ ] Format validation implemented (regex patterns)

- [ ] Length limits enforced

- [ ] Range limits enforced (numeric values)

- [ ] Business logic validation implemented

- [ ] Error messages don't leak information

- [ ] Validation happens server-side (client-side is UI only)

### Output Escaping

- [ ] HTML content escaped in templates

- [ ] HTML attributes properly escaped

- [ ] JavaScript strings properly escaped (JSON.stringify)

- [ ] URL parameters properly encoded

- [ ] CSS values whitelisted/sanitized

- [ ] No direct string concatenation for HTML

- [ ] JSON responses use jsonify()

- [ ] CSV/Excel export properly escaped

### XSS Prevention

- [ ] Jinja2 auto-escaping enabled

- [ ] Content-Security-Policy header set

- [ ] X-XSS-Protection header set

- [ ] X-Content-Type-Options: nosniff set

- [ ] No innerHTML usage in JavaScript

- [ ] No eval() or similar dynamic code execution

- [ ] Markdown sanitized with bleach

- [ ] Event handlers validated

### SQL Injection Prevention

- [ ] No string concatenation in SQL queries

- [ ] ORM (SQLAlchemy) used for queries

- [ ] Parameterized queries for raw SQL

- [ ] Input validated before database queries

- [ ] Database user has minimal privileges

- [ ] SQL errors don't expose schema

### Command Injection Prevention

- [ ] No string concatenation in shell commands

- [ ] subprocess.run() with shell=False

- [ ] Command arguments as list, not string

- [ ] Input validated before command execution

- [ ] Avoid shell=True completely

### Third-party Libraries

- [ ] Dependencies in requirements.txt

- [ ] Versions pinned (no wildcards)

- [ ] Regular pip-audit for vulnerabilities

- [ ] Security patches applied promptly

- [ ] Deprecated libraries replaced

- --

### Testing Commands

## Find SQL injection risks

    grep -r "\.execute\|\.query\|f\".*SELECT\|f'.*SELECT" --include="*.py" .

## Find potential XSS risks

    grep -r "Markup(\|unsafe=\|render_template_string" --include="*.py" .

## Find command injection risks

    grep -r "shell=True\|os.system\|exec(" --include="*.py" .

## Check dependencies for vulnerabilities

    pip install pip-audit
    pip-audit

## Run security scan

    pip install bandit
    bandit -r . -ll
