import streamlit as st
import xml.sax as sax
import requests
import xmlschema

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

    st.title("XSD-to-XML Generator and Schema Documentation")

    # Dropdown options for predefined XSD files
    predefined_xsd_options = {
        "FAIA Reduced Version A": "https://github.com/Tax-Technology/XSD-to-XML-Generator/raw/main/FAIA_v_2.01_reduced_version_A.xsd",
        "FAIA Reduced Version B": "https://github.com/Tax-Technology/XSD-to-XML-Generator/raw/main/FAIA_v_2.01_reduced_version_B.xsd",
        "FAIA Full Version": "https://github.com/Tax-Technology/XSD-to-XML-Generator/raw/main/FAIA_v_2.01_full.xsd"
    }
    selected_predefined_xsd = st.selectbox("Choose a predefined XSD file:", list(predefined_xsd_options.keys()))

    xsd_content = requests.get(predefined_xsd_options[selected_predefined_xsd]).text

    if xsd_content:
        try:
            # Create an XMLSchema object for the XSD schema
            xsd = xmlschema.XMLSchema(xsd_content)

            # Display schema documentation using Streamlit markdown
            st.write("### Schema Documentation")
            st.write("Schema Elements:")
            for element_name in xsd.elements:
                st.write(f"- {element_name}")

            st.write("Schema Attributes:")
            for attr_name in xsd.attributes:
                st.write(f"- {attr_name}")

            st.write("Schema Types:")
            for type_name in xsd.types:
                st.write(f"- {type_name}")

            # Generate the XML document.
            xml_document = generate_xml(xsd_content)

            # Display the generated XML using Streamlit markdown.
            st.write("### Generated XML")
            st.code(xml_document, language="xml")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == '__main__':
    main()
