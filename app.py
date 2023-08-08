import streamlit as st
import xml.sax as sax
import requests

class MyContentHandler(sax.ContentHandler):
    def __init__(self):
        sax.ContentHandler.__init__(self)
        self.xml_output = []

    def startElement(self, name, attrs=None):
        self.xml_output.append(f"<{name}>")

    def endElement(self, name):
        self.xml_output.append(f"</{name}>")

    def characters(self, content):
        self.xml_output.append(content)

    def get_xml(self):
        return "".join(self.xml_output)

def generate_xml(xsd_content: str):
    """Generates an XML document from XSD content.

    Args:
        xsd_content: The content of the XSD file as a string.

    Returns:
        The XML document.
    """
    try:
        # Create a XSD parser.
        parser = sax.make_parser()

        # Set the ContentHandler to our custom handler
        content_handler = MyContentHandler()
        parser.setContentHandler(content_handler)

        # Parse the XSD content.
        parser.feed(xsd_content)

        # Get the generated XML from the custom handler
        xml_document = content_handler.get_xml()

        return xml_document
    except Exception as e:
        raise Exception(f"Error generating XML: {e}")

def main():
    """The main function."""

    # Get user's choice of XSD input method
    xsd_input_method = st.radio(
        "Choose XSD input method:",
        ("Local File Path", "URL", "File Upload", "Sample XSD")
    )

    if xsd_input_method == "Local File Path":
        xsd_content = open(st.text_input('Enter the path to the local XSD file:'), 'r').read()
    elif xsd_input_method == "URL":
        xsd_content = requests.get(st.text_input('Enter the URL to the XSD file:')).text
    elif xsd_input_method == "File Upload":
        xsd_file = st.file_uploader('Upload XSD File', type=['xsd'])
        if xsd_file:
            xsd_content = xsd_file.read().decode('utf-8')
    else:
        # Use the predefined sample XSD from the provided URL
        sample_xsd_url = "https://github.com/Tax-Technology/XSD-to-XML-Generator/raw/main/FAIA_v_2.01_full.xsd"
        xsd_content = requests.get(sample_xsd_url).text

    if xsd_content:
        try:
            # Generate the XML document.
            xml_document = generate_xml(xsd_content)

            # Display the generated XML using Streamlit markdown.
            st.markdown(f"Generated XML:\n\n```xml\n{xml_document}\n```")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == '__main__':
    main()
