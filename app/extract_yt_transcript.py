from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class TranscriptToPDF:
    def __init__(self, video_id, pdf_file_name):
        """
        Initialize with YouTube video ID and desired PDF file name.
        """
        self.video_id = video_id
        self.pdf_file_name = pdf_file_name
        self.transcript = None
        self.text_formatted = None

    def fetch_transcript(self):
        """
        Fetch the transcript for the given YouTube video ID.
        """
        self.transcript = YouTubeTranscriptApi.get_transcript(self.video_id)

    def format_transcript(self):
        """
        Format the fetched transcript into plain text.
        """
        self.text_formatted = TextFormatter().format_transcript(self.transcript)

    def create_pdf(self):
        """
        Create a PDF file from the formatted transcript.
        """
        pdf = canvas.Canvas(self.pdf_file_name, pagesize=letter)
        width, height = letter
        margin = 40
        line_height = 12

        # Split the formatted text into lines
        lines = self.text_formatted.split('\n')
        x = margin
        y = height - margin

        # Write each line to the PDF, handling page breaks
        for line in lines:
            if y < margin:
                pdf.showPage()
                y = height - margin

            pdf.drawString(x, y, line)
            y -= line_height

        # Save the PDF file
        pdf.save()
        print(f"PDF saved as {self.pdf_file_name}")

    def generate_pdf(self):
        """
        Perform all steps to generate the PDF: fetch, format, and create.
        """
        self.fetch_transcript()
        self.format_transcript()
        self.create_pdf()

def main():
    """
    Main function to initialize and run the TranscriptToPDF class.
    """
    video_id = '6o7b9yyhH7k'
    pdf_file_name = 'de_intro.pdf'
    transcript_to_pdf = TranscriptToPDF(video_id, pdf_file_name)
    transcript_to_pdf.generate_pdf()

if __name__ == "__main__":
    main()
