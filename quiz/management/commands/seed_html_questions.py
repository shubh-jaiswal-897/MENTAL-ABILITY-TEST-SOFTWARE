from django.core.management.base import BaseCommand
from quiz.models import Question, Choice
from quiz.models import Subject


QUESTIONS = [
    ("What does HTML stand for?", [
        ("Hyper Text Markup Language", True),
        ("Home Tool Markup Language", False),
        ("Hyperlinks and Text Markup Language", False),
        ("Hyper Transfer Markup Language", False),
    ]),
    ("Which HTML element is used to define the largest heading?", [
        ("<h1>", True),
        ("<head>", False),
        ("<h6>", False),
        ("<header>", False),
    ]),
    ("Which tag is used to create a hyperlink?", [
        ("<a>", True),
        ("<link>", False),
        ("<href>", False),
        ("<url>", False),
    ]),
    ("Which attribute is used to specify an alternate text for an image?", [
        ("alt", True),
        ("title", False),
        ("src", False),
        ("longdesc", False),
    ]),
    ("How do you create a numbered list in HTML?", [
        ("<ol>", True),
        ("<ul>", False),
        ("<li>", False),
        ("<dl>", False),
    ]),
    ("Which doctype is correct for HTML5?", [
        ("<!DOCTYPE html>", True),
        ("<!DOCTYPE HTML PUBLIC\"-//W3C//DTD HTML 4.01//EN\"\">", False),
        ("<DOCTYPE html5>", False),
        ("<!DOCTYPE XHTML>", False),
    ]),
    ("Which element is used to specify a footer for a document or section?", [
        ("<footer>", True),
        ("<bottom>", False),
        ("<section-footer>", False),
        ("<foot>", False),
    ]),
    (("How do you insert a comment in HTML?"), [
        ("<!-- This is a comment -->", True),
        ("// This is a comment", False),
        ("/* This is a comment */", False),
        ("# This is a comment", False),
    ]),
    ("Which tag is used to display a picture on a web page?", [
        ("<img>", True),
        ("<picture>", False),
        ("<image>", False),
        ("<src>", False),
    ]),
    ("Which HTML attribute is used to define inline styles?", [
        ("style", True),
        ("class", False),
        ("font", False),
        ("styles", False),
    ]),
    ("Which element defines navigation links?", [
        ("<nav>", True),
        ("<navigate>", False),
        ("<navigation>", False),
        ("<menu>", False),
    ]),
    ("How can you open a link in a new tab/browser window?", [
        ("Use target=\"_blank\" on the <a> tag", True),
        ("Use rel=\"external\" on the <a> tag", False),
        ("Use newtab=\"true\"", False),
        ("Use href=\"_blank\"", False),
    ]),
    ("Which HTML element is used to specify a scalar measurement within text?", [
        ("<meter>", True),
        ("<measure>", False),
        ("<progress>", False),
        ("<gauge>", False),
    ]),
    ("Which element is used to embed a video in HTML5?", [
        ("<video>", True),
        ("<media>", False),
        ("<movie>", False),
        ("<embed>", False),
    ]),
    ("What is the correct HTML element for playing audio files?", [
        ("<audio>", True),
        ("<sound>", False),
        ("<play>", False),
        ("<media>", False),
    ]),
    ("Which attribute is used to specify the URL of an image?", [
        ("src", True),
        ("href", False),
        ("link", False),
        ("url", False),
    ]),
    ("Which tag is used to define an internal style sheet?", [
        ("<style>", True),
        ("<css>", False),
        ("<script>", False),
        ("<link>", False),
    ]),
    ("Which HTML element is used to define important text?", [
        ("<strong>", True),
        ("<b>", False),
        ("<important>", False),
        ("<i>", False),
    ]),
    ("Which tag is used to create a checkbox in a form?", [
        ("<input type=\"checkbox\">", True),
        ("<checkbox>", False),
        ("<input type=\"check\">", False),
        ("<check>", False),
    ]),
    ("How do you create a drop-down list in HTML?", [
        ("<select>", True),
        ("<dropdown>", False),
        ("<list>", False),
        ("<optionlist>", False),
    ]),
    ("Which attribute is used to provide a unique identifier to an HTML element?", [
        ("id", True),
        ("class", False),
        ("name", False),
        ("key", False),
    ]),
    ("Which element is used to group related elements in a form?", [
        ("<fieldset>", True),
        ("<group>", False),
        ("<formgroup>", False),
        ("<legend>", False),
    ]),
    ("Which tag is used to define a table row?", [
        ("<tr>", True),
        ("<td>", False),
        ("<table-row>", False),
        ("<row>", False),
    ]),
    ("Which tag defines a table header cell?", [
        ("<th>", True),
        ("<td>", False),
        ("<thead>", False),
        ("<header>", False),
    ]),
    ("Which tag is used to group the body content in a table?", [
        ("<tbody>", True),
        ("<thead>", False),
        ("<tfoot>", False),
        ("<tablebody>", False),
    ]),
    ("Which attribute is used to specify the language of the document?", [
        ("lang", True),
        ("xml:lang", False),
        ("language", False),
        ("locale", False),
    ]),
    ("Which HTML element is used to specify a section that is quoted from another source?", [
        ("<blockquote>", True),
        ("<q>", False),
        ("<cite>", False),
        ("<quote>", False),
    ]),
]


class Command(BaseCommand):
    help = 'Seed 30 HTML-related questions into the quiz app (idempotent)'

    def handle(self, *args, **options):
        created = 0
        html_subj, _ = Subject.objects.get_or_create(name='HTML')
        Subject.objects.get_or_create(name='CSS')
        Subject.objects.get_or_create(name='JavaScript')
        for q_text, choices in QUESTIONS:
            q, q_created = Question.objects.get_or_create(text=q_text, defaults={'subject': html_subj})
            if q_created:
                created += 1
            # create choices, avoid duplicates
            for choice_text, is_correct in choices:
                Choice.objects.get_or_create(question=q, text=choice_text, defaults={'is_correct': is_correct})

        self.stdout.write(self.style.SUCCESS(f'Seed completed. Questions created: {created}'))
