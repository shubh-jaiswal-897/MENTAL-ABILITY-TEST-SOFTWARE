from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Replace generated placeholder questions with curated, original questions per subject.'

    def handle(self, *args, **options):
        from quiz.models import Subject, Question, Choice

        data = {
            'HTML': [
                ("What does HTML stand for?",
                 ["Hyper Text Markup Language", "Hyperlinks and Text Markup Language", "Home Tool Markup Language", "Hyperlinking Text Markup Language"], 0),
                ("Which tag is used to create a hyperlink?",
                 ["<a>", "<link>", "<href>", "<url>"], 0),
                ("Which element is used for the largest heading?",
                 ["<h1>", "<h6>", "<title>", "<head>"], 0),
                ("What attribute is used to specify alternate text for an image?",
                 ["alt", "title", "src", "caption"], 0),
                ("Which tag is used to create an ordered list?",
                 ["<ol>", "<ul>", "<li>", "<list>"], 0),
                ("Which attribute provides a unique identifier for an element?",
                 ["id", "class", "name", "key"], 0),
                ("What is the correct HTML element for inserting a line break?",
                 ["<br>", "<break>", "<lb>", "<newline>"], 0),
                ("Which HTML tag is used to define an unordered list?",
                 ["<ul>", "<ol>", "<li>", "<list>"], 0),
                ("How do you create a checkbox in HTML?",
                 ["<input type='checkbox'>", "<checkbox>", "<input checkbox>", "<check>"], 0),
                ("Which attribute specifies the URL of an external script file?",
                 ["src", "href", "link", "file"], 0),
            ],
            'CSS': [
                ("What does CSS stand for?",
                 ["Cascading Style Sheets", "Computer Style Sheets", "Creative Style System", "Colorful Style Sheets"], 0),
                ("Which property is used to change the text color of an element?",
                 ["color", "font-color", "text-color", "fg-color"], 0),
                ("How do you select an element with id 'header' in CSS?",
                 ["#header", ".header", "header", "*header"], 0),
                ("Which CSS property controls the layout flow (flex/grid)?",
                 ["display", "position", "float", "layout"], 0),
                ("How do you make text bold using CSS?",
                 ["font-weight: bold;", "text-style: bold;", "font-style: bold;", "text-weight: bold;"], 0),
                ("Which property adds space inside an element's border?",
                 ["padding", "margin", "gap", "spacing"], 0),
                ("Which property is used to change the font size?",
                 ["font-size", "text-size", "font-style", "size"], 0),
                ("How do you apply a style only when hovering over an element?",
                 [":hover", ":focus", ":active", ":visited"], 0),
                ("Which unit is relative to the root element's font size?",
                 ["rem", "em", "px", "%"], 0),
                ("How do you center a block element horizontally with CSS?",
                 ["margin: 0 auto;", "text-align: center;", "align:center;", "center: true;"], 0),
            ],
            'JavaScript': [
                ("Which keyword declares a block-scoped variable in modern JavaScript?",
                 ["let", "var", "consts", "constant"], 0),
                ("How do you write a function named 'sum' that returns a+b?",
                 ["function sum(a, b) { return a + b; }", "def sum(a,b): return a+b", "func sum(a,b) => a+b", "sum = (a,b) => a + b"], 0),
                ("Which method converts a JSON string to a JavaScript object?",
                 ["JSON.parse", "JSON.stringify", "parseJSON", "toObject"], 0),
                ("What is the result type of 'typeof []' in JavaScript?",
                 ["object", "array", "list", "undefined"], 0),
                ("Which event fires when the user clicks on an element?",
                 ["click", "change", "submit", "load"], 0),
                ("Which operator is used for strict equality (no type coercion)?",
                 ["===", "==", "=", "!=="], 0),
                ("How do you add an element to the end of an array 'arr'?",
                 ["arr.push(item)", "arr.add(item)", "arr.insert(item)", "arr.append(item)"], 0),
                ("Which keyword is used to create a promise in JS?",
                 ["new Promise", "promise()", "create Promise", "Promise.make"], 0),
                ("Which method schedules a function to run after a delay?",
                 ["setTimeout", "setInterval", "delay", "defer"], 0),
                ("What will 'console.log(typeof null)' output?",
                 ["object", "null", "undefined", "number"], 0),
            ],
            'Bootstrap': [
                ("Bootstrap is primarily a _____ framework.",
                 ["CSS","JavaScript","Database","Backend"], 0),
                ("Which class creates a responsive container that adapts to viewport?",
                 ["container-fluid", "container-fixed", "container-adaptive", "container-responsive"], 0),
                ("Which Bootstrap class creates a button with primary styling?",
                 ["btn btn-primary", "button-primary", "btn primary", "primary-btn"], 0),
                ("How do you create a responsive grid column that takes half width on md screens?",
                 ["col-md-6", "col-6-md", "md-col-6", "col-half-md"], 0),
                ("Which utility class adds margin on top (mt) with value 3?",
                 ["mt-3", "m-top-3", "margin-top-3", "top-margin-3"], 0),
                ("Bootstrap's JS components require which dependency (Bootstrap 4)?",
                 ["Popper.js", "jQuery UI", "Lodash", "Axios"], 0),
                ("Which class makes an image responsive in Bootstrap?",
                 ["img-fluid", "img-responsive", "responsive-img", "img-scale"], 0),
                ("How do you create a Bootstrap navbar?",
                 ["Use <nav class='navbar'> with container and toggler", "Use <navbar> tag", "Use <div class='nav'> only", "Use <menu> tag"], 0),
                ("Which class aligns text to the center in Bootstrap?",
                 ["text-center", "center-text", "align-center", "text-align-center"], 0),
                ("Which grid class hides an element on small screens?",
                 ["d-none d-sm-block", "hidden-sm", "hide-sm", "d-hide-sm"], 0),
            ],
            'Python': [
                ("Which keyword starts a function definition in Python?",
                 ["def", "function", "fun", "proc"], 0),
                ("How do you create a list with numbers 1 to 3?",
                 ["[1, 2, 3]", "(1,2,3)", "{1,2,3}", "list(1,2,3)"], 0),
                ("Which statement is used for conditional execution?",
                 ["if", "when", "case", "cond"], 0),
                ("How do you open a file 'f.txt' for reading?",
                 ["open('f.txt', 'r')", "open('f.txt')", "file('f.txt','r')", "read('f.txt')"], 0),
                ("Which built-in converts a value to an integer?",
                 ["int()", "integer()", "to_int()", "cast_int()"], 0),
                ("How do you write a for-loop over items in a list 'items'?",
                 ["for x in items:", "for (x in items):", "foreach items as x:", "loop x in items:"], 0),
                ("Which data type is immutable in Python?",
                 ["tuple", "list", "dict", "set"], 0),
                ("How do you add an element to the end of a list 'lst'?",
                 ["lst.append(x)", "lst.add(x)", "lst.push(x)", "append(lst,x)"], 0),
                ("Which keyword is used to handle exceptions?",
                 ["try/except", "catch", "handle", "onerror"], 0),
                ("How do you import the math module?",
                 ["import math", "include math", "require 'math'", "from math import *"], 0),
            ],
        }

        subjects = Subject.objects.all()
        if not subjects:
            self.stdout.write(self.style.WARNING('No subjects found. Create subjects first.'))
            return

        for subject in subjects:
            name = subject.name
            items = data.get(name)
            if not items:
                self.stdout.write(self.style.WARNING(f'No curated data for subject {name}, skipping.'))
                continue

            # Remove placeholder generated questions for this subject
            placeholders = Question.objects.filter(subject=subject, text__icontains='Generated Question')
            removed = placeholders.count()
            placeholders.delete()

            created = 0
            for q_text, options, correct_idx in items:
                q, q_created = Question.objects.get_or_create(text=q_text, subject=subject)
                # Remove existing choices if any and recreate to match curated options
                if not q_created:
                    Choice.objects.filter(question=q).delete()
                for idx, opt in enumerate(options):
                    Choice.objects.create(question=q, text=opt, is_correct=(idx == correct_idx))
                if q_created:
                    created += 1

            total = Question.objects.filter(subject=subject).count()
            self.stdout.write(self.style.SUCCESS(
                f"Subject '{name}': removed {removed} placeholders, added/updated {len(items)} curated questions (total {total})."
            ))

        self.stdout.write(self.style.SUCCESS('Replacement with curated questions complete.'))
