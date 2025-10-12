from django.core.management.base import BaseCommand
from quiz.models import Subject, Question, Choice

class Command(BaseCommand):
    help = 'Seed Bootstrap questions'

    def handle(self, *args, **options):
        # Create subject if not exists
        subject, created = Subject.objects.get_or_create(name='Bootstrap')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created subject: {subject.name}'))
        else:
            self.stdout.write(f'Subject {subject.name} already exists')

        # Delete existing questions for this subject
        Question.objects.filter(subject=subject).delete()
        self.stdout.write(f'Deleted existing questions for {subject.name}')

        # Questions data
        questions_data = [
            {
                'text': 'What is Bootstrap?',
                'choices': ['A CSS framework', 'A JavaScript library', 'A database', 'An operating system'],
                'correct': 0
            },
            {
                'text': 'Which company developed Bootstrap?',
                'choices': ['Google', 'Microsoft', 'Twitter', 'Facebook'],
                'correct': 2
            },
            {
                'text': 'What is the latest stable version of Bootstrap?',
                'choices': ['Bootstrap 3', 'Bootstrap 4', 'Bootstrap 5', 'Bootstrap 6'],
                'correct': 2
            },
            {
                'text': 'Which class is used for creating a responsive container in Bootstrap?',
                'choices': ['.container', '.wrapper', '.box', '.frame'],
                'correct': 0
            },
            {
                'text': 'What does the Bootstrap grid system use?',
                'choices': ['Pixels', 'Percentages', 'Flexbox', 'Tables'],
                'correct': 2
            },
            {
                'text': 'How many columns does Bootstrap\'s grid system have?',
                'choices': ['10', '12', '14', '16'],
                'correct': 1
            },
            {
                'text': 'Which class is used to create a button in Bootstrap?',
                'choices': ['.btn', '.button', '.link', '.click'],
                'correct': 0
            },
            {
                'text': 'What is the default size of a Bootstrap button?',
                'choices': ['Small', 'Medium', 'Large', 'Extra Large'],
                'correct': 1
            },
            {
                'text': 'Which class is used for creating a navigation bar in Bootstrap?',
                'choices': ['.nav', '.navbar', '.menu', '.header'],
                'correct': 1
            },
            {
                'text': 'What is the purpose of Bootstrap\'s responsive utilities?',
                'choices': ['To hide elements on different screen sizes', 'To show elements on different screen sizes', 'Both A and B', 'None of the above'],
                'correct': 2
            },
            {
                'text': 'Which class is used to create a modal in Bootstrap?',
                'choices': ['.modal', '.popup', '.dialog', '.window'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component used for displaying tabular data?',
                'choices': ['Table', 'List', 'Card', 'Panel'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a card in Bootstrap?',
                'choices': ['.card', '.box', '.panel', '.tile'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility class for adding margin?',
                'choices': ['.m-*', '.margin-*', '.space-*', '.pad-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a dropdown in Bootstrap?',
                'choices': ['.dropdown', '.select', '.menu', '.list'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying alerts?',
                'choices': ['.alert', '.message', '.notification', '.info'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a progress bar in Bootstrap?',
                'choices': ['.progress', '.bar', '.status', '.load'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for text alignment?',
                'choices': ['.text-*', '.align-*', '.position-*', '.float-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a carousel in Bootstrap?',
                'choices': ['.carousel', '.slider', '.gallery', '.show'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for grouping buttons?',
                'choices': ['Button group', 'Button set', 'Button collection', 'Button array'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a badge in Bootstrap?',
                'choices': ['.badge', '.tag', '.label', '.mark'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for floating elements?',
                'choices': ['.float-*', '.position-*', '.align-*', '.move-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a tooltip in Bootstrap?',
                'choices': ['.tooltip', '.hint', '.info', '.help'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying breadcrumbs?',
                'choices': ['.breadcrumb', '.path', '.nav', '.trail'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a pagination in Bootstrap?',
                'choices': ['.pagination', '.pages', '.nav', '.links'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for border radius?',
                'choices': ['.rounded', '.border-radius', '.curve', '.arc'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a spinner in Bootstrap?',
                'choices': ['.spinner', '.loader', '.wait', '.busy'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying toasts?',
                'choices': ['.toast', '.notification', '.alert', '.message'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a collapse in Bootstrap?',
                'choices': ['.collapse', '.hide', '.fold', '.minimize'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for display properties?',
                'choices': ['.d-*', '.show-*', '.visible-*', '.block-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a list group in Bootstrap?',
                'choices': ['.list-group', '.group', '.collection', '.set'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying media objects?',
                'choices': ['.media', '.object', '.item', '.content'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a jumbotron in Bootstrap?',
                'choices': ['.jumbotron', '.hero', '.banner', '.header'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for flexbox?',
                'choices': ['.d-flex', '.flex', '.flexbox', '.layout'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a popover in Bootstrap?',
                'choices': ['.popover', '.popup', '.tip', '.info'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying forms?',
                'choices': ['Form', 'Input', 'Field', 'Control'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a form group in Bootstrap?',
                'choices': ['.form-group', '.group', '.section', '.block'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for text color?',
                'choices': ['.text-*', '.color-*', '.font-*', '.style-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a input group in Bootstrap?',
                'choices': ['.input-group', '.group', '.set', '.collection'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying custom checkboxes?',
                'choices': ['.custom-checkbox', '.checkbox', '.check', '.select'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a custom file input in Bootstrap?',
                'choices': ['.custom-file', '.file', '.upload', '.input'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for background color?',
                'choices': ['.bg-*', '.background-*', '.color-*', '.fill-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a custom select in Bootstrap?',
                'choices': ['.custom-select', '.select', '.dropdown', '.choice'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying ranges?',
                'choices': ['.custom-range', '.range', '.slider', '.bar'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a form control in Bootstrap?',
                'choices': ['.form-control', '.control', '.input', '.field'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for font weight?',
                'choices': ['.font-weight-*', '.weight-*', '.bold-*', '.strong-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a form check in Bootstrap?',
                'choices': ['.form-check', '.check', '.select', '.option'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying validation?',
                'choices': ['.valid-*', '.invalid-*', '.is-valid', '.is-invalid'],
                'correct': 2
            },
            {
                'text': 'Which class is used to create a form text in Bootstrap?',
                'choices': ['.form-text', '.text', '.help', '.info'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for border?',
                'choices': ['.border', '.line', '.edge', '.frame'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a border in Bootstrap?',
                'choices': ['.border', '.outline', '.frame', '.edge'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for border color?',
                'choices': ['.border-*', '.color-*', '.line-*', '.edge-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a border width in Bootstrap?',
                'choices': ['.border-*', '.width-*', '.size-*', '.thick-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying shadows?',
                'choices': ['.shadow', '.depth', '.elevation', '.layer'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a shadow in Bootstrap?',
                'choices': ['.shadow', '.shade', '.dark', '.blur'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for position?',
                'choices': ['.position-*', '.place-*', '.locate-*', '.set-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a fixed position in Bootstrap?',
                'choices': ['.fixed-*', '.position-fixed', '.static', '.relative'],
                'correct': 1
            },
            {
                'text': 'What is the Bootstrap utility for sizing?',
                'choices': ['.w-*', '.h-*', '.size-*', '.dimension-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a width in Bootstrap?',
                'choices': ['.w-*', '.width-*', '.size-*', '.expand-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying utilities?',
                'choices': ['Spacing', 'Color', 'Typography', 'All of the above'],
                'correct': 3
            },
            {
                'text': 'Which class is used to create a margin in Bootstrap?',
                'choices': ['.m-*', '.margin-*', '.space-*', '.gap-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for padding?',
                'choices': ['.p-*', '.padding-*', '.space-*', '.fill-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a padding in Bootstrap?',
                'choices': ['.p-*', '.pad-*', '.space-*', '.fill-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying flex utilities?',
                'choices': ['.d-flex', '.flex-*', '.justify-*', '.align-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a flex container in Bootstrap?',
                'choices': ['.d-flex', '.flex', '.container', '.box'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for justify content?',
                'choices': ['.justify-content-*', '.align-*', '.flex-*', '.position-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a justify content in Bootstrap?',
                'choices': ['.justify-content-*', '.align-*', '.center-*', '.position-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying grid?',
                'choices': ['.container', '.row', '.col-*', 'All of the above'],
                'correct': 3
            },
            {
                'text': 'Which class is used to create a container in Bootstrap?',
                'choices': ['.container', '.wrapper', '.box', '.frame'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for columns?',
                'choices': ['.col-*', '.column-*', '.grid-*', '.cell-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a column in Bootstrap?',
                'choices': ['.col-*', '.column-*', '.grid-*', '.cell-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying breakpoints?',
                'choices': ['sm', 'md', 'lg', 'xl'],
                'correct': 0
            },
            {
                'text': 'Which breakpoint is for small screens in Bootstrap?',
                'choices': ['sm', 'md', 'lg', 'xl'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for responsive images?',
                'choices': ['.img-fluid', '.responsive', '.fluid', '.auto'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a responsive image in Bootstrap?',
                'choices': ['.img-fluid', '.responsive', '.fluid', '.auto'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying figures?',
                'choices': ['.figure', '.image', '.photo', '.pic'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a figure in Bootstrap?',
                'choices': ['.figure', '.image', '.photo', '.pic'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for embedding?',
                'choices': ['.embed-responsive', '.video', '.media', '.iframe'],
                'correct': 0
            },
            {
                'text': 'Which class is used for creating a responsive embed in Bootstrap?',
                'choices': ['.embed-responsive', '.responsive', '.video', '.media'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying close button?',
                'choices': ['.close', '.x', '.exit', '.cancel'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a close button in Bootstrap?',
                'choices': ['.close', '.x', '.exit', '.cancel'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for screen readers?',
                'choices': ['.sr-only', '.hidden', '.invisible', '.none'],
                'correct': 0
            },
            {
                'text': 'Which class is used for screen reader only content in Bootstrap?',
                'choices': ['.sr-only', '.hidden', '.invisible', '.none'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying print utilities?',
                'choices': ['.d-print-*', '.print-*', '.show-print', '.visible-print'],
                'correct': 0
            },
            {
                'text': 'Which class is used to hide elements when printing in Bootstrap?',
                'choices': ['.d-print-none', '.print-none', '.hide-print', '.invisible-print'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for overflow?',
                'choices': ['.overflow-*', '.scroll-*', '.flow-*', '.wrap-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for overflow hidden in Bootstrap?',
                'choices': ['.overflow-hidden', '.hidden', '.no-scroll', '.clip'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying vertical alignment?',
                'choices': ['.align-*', '.vertical-*', '.position-*', '.center-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used to align items vertically in Bootstrap?',
                'choices': ['.align-items-*', '.vertical-*', '.center-*', '.position-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for text decoration?',
                'choices': ['.text-decoration-*', '.underline-*', '.line-*', '.style-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for text decoration none in Bootstrap?',
                'choices': ['.text-decoration-none', '.no-decoration', '.plain', '.clean'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying font size?',
                'choices': ['.fs-*', '.font-size-*', '.size-*', '.text-size-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used to set font size in Bootstrap?',
                'choices': ['.fs-*', '.font-*', '.size-*', '.text-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for line height?',
                'choices': ['.lh-*', '.line-height-*', '.height-*', '.spacing-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for line height in Bootstrap?',
                'choices': ['.lh-*', '.line-*', '.height-*', '.spacing-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying text transform?',
                'choices': ['.text-*', '.transform-*', '.case-*', '.style-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for text lowercase in Bootstrap?',
                'choices': ['.text-lowercase', '.lowercase', '.small', '.down'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for font style?',
                'choices': ['.fst-*', '.font-style-*', '.style-*', '.italic-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for italic text in Bootstrap?',
                'choices': ['.fst-italic', '.italic', '.slant', '.style'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying ratios?',
                'choices': ['.ratio', '.aspect', '.size', '.dimension'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create aspect ratios in Bootstrap?',
                'choices': ['.ratio', '.aspect-*', '.size-*', '.dimension-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for visibility?',
                'choices': ['.visible', '.invisible', '.show', '.hide'],
                'correct': 1
            },
            {
                'text': 'Which class is used to make elements invisible in Bootstrap?',
                'choices': ['.invisible', '.hidden', '.none', '.transparent'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying opacity?',
                'choices': ['.opacity-*', '.transparent-*', '.fade-*', '.blur-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for opacity in Bootstrap?',
                'choices': ['.opacity-*', '.fade-*', '.transparent-*', '.blur-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for z-index?',
                'choices': ['.z-*', '.index-*', '.layer-*', '.depth-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for z-index in Bootstrap?',
                'choices': ['.z-*', '.index-*', '.layer-*', '.depth-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying transitions?',
                'choices': ['.transition-*', '.animate-*', '.move-*', '.change-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for transitions in Bootstrap?',
                'choices': ['.transition-*', '.animate-*', '.move-*', '.change-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for transforms?',
                'choices': ['.transform-*', '.rotate-*', '.scale-*', '.skew-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for transforms in Bootstrap?',
                'choices': ['.transform-*', '.rotate-*', '.scale-*', '.skew-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying animations?',
                'choices': ['.animate-*', '.motion-*', '.move-*', '.action-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for animations in Bootstrap?',
                'choices': ['.animate-*', '.motion-*', '.move-*', '.action-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for user select?',
                'choices': ['.user-select-*', '.select-*', '.choose-*', '.pick-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for user select none in Bootstrap?',
                'choices': ['.user-select-none', '.no-select', '.unselectable', '.disabled'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying pointer events?',
                'choices': ['.pe-*', '.pointer-*', '.event-*', '.click-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for pointer events none in Bootstrap?',
                'choices': ['.pe-none', '.no-pointer', '.disabled', '.inactive'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for resize?',
                'choices': ['.resize', '.adjust', '.size', '.change'],
                'correct': 0
            },
            {
                'text': 'Which class is used for resize none in Bootstrap?',
                'choices': ['.resize-none', '.no-resize', '.fixed', '.static'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying vertical rule?',
                'choices': ['.vr', '.line', '.divider', '.separator'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a vertical rule in Bootstrap?',
                'choices': ['.vr', '.vertical', '.line', '.divider'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for text truncation?',
                'choices': ['.text-truncate', '.truncate', '.short', '.cut'],
                'correct': 0
            },
            {
                'text': 'Which class is used for text truncation in Bootstrap?',
                'choices': ['.text-truncate', '.truncate', '.short', '.cut'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying stretched link?',
                'choices': ['.stretched-link', '.link', '.extend', '.full'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a stretched link in Bootstrap?',
                'choices': ['.stretched-link', '.link', '.extend', '.full'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for object fit?',
                'choices': ['.object-fit-*', '.fit-*', '.size-*', '.adjust-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for object fit cover in Bootstrap?',
                'choices': ['.object-fit-cover', '.cover', '.fit', '.adjust'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying focus ring?',
                'choices': ['.focus-ring', '.ring', '.focus', '.highlight'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a focus ring in Bootstrap?',
                'choices': ['.focus-ring', '.ring', '.focus', '.highlight'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for text reset?',
                'choices': ['.text-reset', '.reset', '.clear', '.default'],
                'correct': 0
            },
            {
                'text': 'Which class is used for text reset in Bootstrap?',
                'choices': ['.text-reset', '.reset', '.clear', '.default'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying ratio 16x9?',
                'choices': ['.ratio-16x9', '.16x9', '.wide', '.cinema'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a 16x9 ratio in Bootstrap?',
                'choices': ['.ratio-16x9', '.16x9', '.wide', '.cinema'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for text opacity?',
                'choices': ['.text-opacity-*', '.opacity-*', '.fade-*', '.transparent-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for text opacity in Bootstrap?',
                'choices': ['.text-opacity-*', '.opacity-*', '.fade-*', '.transparent-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying link opacity?',
                'choices': ['.link-opacity-*', '.opacity-*', '.fade-*', '.transparent-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for link opacity in Bootstrap?',
                'choices': ['.link-opacity-*', '.opacity-*', '.fade-*', '.transparent-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for border opacity?',
                'choices': ['.border-opacity-*', '.opacity-*', '.fade-*', '.transparent-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for border opacity in Bootstrap?',
                'choices': ['.border-opacity-*', '.opacity-*', '.fade-*', '.transparent-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying focus ring opacity?',
                'choices': ['.focus-ring-opacity-*', '.opacity-*', '.fade-*', '.transparent-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for focus ring opacity in Bootstrap?',
                'choices': ['.focus-ring-opacity-*', '.opacity-*', '.fade-*', '.transparent-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for box shadow?',
                'choices': ['.box-shadow-*', '.shadow-*', '.depth-*', '.elevation-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for box shadow in Bootstrap?',
                'choices': ['.box-shadow-*', '.shadow-*', '.depth-*', '.elevation-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying text shadow?',
                'choices': ['.text-shadow', '.shadow', '.depth', '.elevation'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a text shadow in Bootstrap?',
                'choices': ['.text-shadow', '.shadow', '.depth', '.elevation'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for glow?',
                'choices': ['.glow', '.shine', '.bright', '.light'],
                'correct': 0
            },
            {
                'text': 'Which class is used for glow in Bootstrap?',
                'choices': ['.glow', '.shine', '.bright', '.light'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying focus glow?',
                'choices': ['.focus-glow', '.glow', '.shine', '.bright'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a focus glow in Bootstrap?',
                'choices': ['.focus-glow', '.glow', '.shine', '.bright'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for backdrop?',
                'choices': ['.backdrop', '.background', '.layer', '.overlay'],
                'correct': 0
            },
            {
                'text': 'Which class is used for backdrop in Bootstrap?',
                'choices': ['.backdrop', '.background', '.layer', '.overlay'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying offcanvas?',
                'choices': ['.offcanvas', '.sidebar', '.drawer', '.panel'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create an offcanvas in Bootstrap?',
                'choices': ['.offcanvas', '.sidebar', '.drawer', '.panel'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for placeholder?',
                'choices': ['.placeholder', '.hint', '.sample', '.example'],
                'correct': 0
            },
            {
                'text': 'Which class is used for placeholder in Bootstrap?',
                'choices': ['.placeholder', '.hint', '.sample', '.example'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying accordion?',
                'choices': ['.accordion', '.collapse', '.panel', '.group'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create an accordion in Bootstrap?',
                'choices': ['.accordion', '.collapse', '.panel', '.group'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for scrollspy?',
                'choices': ['.scrollspy', '.spy', '.track', '.follow'],
                'correct': 0
            },
            {
                'text': 'Which class is used for scrollspy in Bootstrap?',
                'choices': ['.scrollspy', '.spy', '.track', '.follow'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying tabs?',
                'choices': ['.nav-tabs', '.tabs', '.menu', '.list'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create tabs in Bootstrap?',
                'choices': ['.nav-tabs', '.tabs', '.menu', '.list'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for pills?',
                'choices': ['.nav-pills', '.pills', '.buttons', '.links'],
                'correct': 0
            },
            {
                'text': 'Which class is used for nav pills in Bootstrap?',
                'choices': ['.nav-pills', '.pills', '.buttons', '.links'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying navbar?',
                'choices': ['.navbar', '.nav', '.menu', '.header'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a navbar in Bootstrap?',
                'choices': ['.navbar', '.nav', '.menu', '.header'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for navbar brand?',
                'choices': ['.navbar-brand', '.brand', '.logo', '.title'],
                'correct': 0
            },
            {
                'text': 'Which class is used for navbar brand in Bootstrap?',
                'choices': ['.navbar-brand', '.brand', '.logo', '.title'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying navbar nav?',
                'choices': ['.navbar-nav', '.nav', '.menu', '.list'],
                'correct': 0
            },
            {
                'text': 'Which class is used for navbar nav in Bootstrap?',
                'choices': ['.navbar-nav', '.nav', '.menu', '.list'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for navbar toggler?',
                'choices': ['.navbar-toggler', '.toggler', '.button', '.switch'],
                'correct': 0
            },
            {
                'text': 'Which class is used for navbar toggler in Bootstrap?',
                'choices': ['.navbar-toggler', '.toggler', '.button', '.switch'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying navbar collapse?',
                'choices': ['.navbar-collapse', '.collapse', '.hide', '.fold'],
                'correct': 0
            },
            {
                'text': 'Which class is used for navbar collapse in Bootstrap?',
                'choices': ['.navbar-collapse', '.collapse', '.hide', '.fold'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap utility for navbar expand?',
                'choices': ['.navbar-expand-*', '.expand-*', '.show-*', '.visible-*'],
                'correct': 0
            },
            {
                'text': 'Which class is used for navbar expand in Bootstrap?',
                'choices': ['.navbar-expand-*', '.expand-*', '.show-*', '.visible-*'],
                'correct': 0
            },
            {
                'text': 'What is the Bootstrap component for displaying breadcrumb?',
                'choices': ['.breadcrumb', '.path', '.nav', '.trail'],
                'correct': 0
            },
            {
                'text': 'Which class is used to create a breadcrumb in Bootstrap?',
                'choices': ['.breadcrumb', '.path', '.nav', '.trail'],
                'correct': 0
            }
        ]

        # Create questions and choices
        for q_data in questions_data:
            question = Question.objects.create(subject=subject, text=q_data['text'])
            for i, choice_text in enumerate(q_data['choices']):
                is_correct = (i == q_data['correct'])
                Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(questions_data)} Bootstrap questions'))
