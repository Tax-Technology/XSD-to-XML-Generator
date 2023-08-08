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
            # Generate the XML document.
            xml_document = generate_xml(xsd_content)

            # Display the generated XML using Streamlit markdown.
            st.markdown(f"Generated XML:\n\n```xml\n{xml_document}\n```")

            # Create an XMLSchema object for the XSD schema
            xsd = xmlschema.XMLSchema(xsd_content)

            # Extract schema information
            schema_info = xsd.schema_info()

            # Display schema documentation using Streamlit markdown
            st.write("### Schema Documentation")
            st.write("Allowed Elements:")
            for element_name, element_info in schema_info.elements.items():
                st.write(f"- {element_name} (Type: {element_info.type_name})")

            st.write("Allowed Attributes:")
            for attr_name, attr_info in schema_info.attributes.items():
                st.write(f"- {attr_name} (Type: {attr_info.type_name})")

            st.write("Type Definitions:")
            for type_name, type_info in schema_info.types.items():
                st.write(f"- {type_name} (Base Type: {type_info.base_type_name})")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == '__main__':
    main()
