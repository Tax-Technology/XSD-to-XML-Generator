import streamlit as st
import xml.sax as sax

class MyContentHandler(sax.ContentHandler):
    def __init__(self):
        sax.ContentHandler.__init__(self)
        self.xml_output = []

    def startElement(self, name, attrs):
        self.xml_output.append(f"<{name}>")

    def endElement(self, name):
        self.xml_output.append(f"</{name}>")

    def characters(self, content):
        self.xml_output.append(content)

    def get_xml(self):
        return "".join(self.xml_output)

def generate_xml(xsd_file):
    """Generates an XML document from a XSD file.

    Args:
        xsd_file: The path to the XSD file.

    Returns:
        The XML document.
    """
    # Create a XSD parser.
    parser = sax.make_parser()

    # Set the ContentHandler to our custom handler
    content_handler = MyContentHandler()
    parser.setContentHandler(content_handler)

    try:
        # Load and parse the XSD file.
        parser.parse(xsd_file)

        # Get the generated XML from the custom handler
        xml_document = content_handler.get_xml()

        return xml_document
    except Exception as e:
        raise Exception(f"Error generating XML: {e}")

def main():
    """The main function."""

    # Get the XSD file path from the user.
    xsd_file = st.text_input('Enter the path to the XSD file:')

    if xsd_file:
        try:
            # Generate the XML document.
            xml_document = generate_xml(xsd_file)

            # Display the generated XML using Streamlit markdown.
            st.markdown(f"Generated XML:\n\n```xml\n{xml_document}\n```")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == '__main__':
    main()
