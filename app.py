import streamlit as st
import xmlschema
import requests

def get_element_info(element, level=0):
    info = f"{'  ' * level}- {element.name} (Type: {element.type_name})"
    for sub_element in element.type.content_type.iter_elements():
        info += "\n" + get_element_info(sub_element, level + 1)
    return info

def get_keyref_info(schema):
    keyref_info = []
    for element_name, element in schema.elements.items():
        if element.keyref:
            for keyref in element.keyref:
                keyref_info.append(f"- Element: {element_name}, Keyref: {keyref.name}")
    return keyref_info

def main():
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

            if xsd.root_elements:
                for root_element_name in xsd.root_elements:
                    root_element = xsd.elements[root_element_name]
                    st.write(f"Root Element: {root_element_name} (Type: {root_element.type_name})")
                    st.write(get_element_info(root_element))

            keyref_info = get_keyref_info(xsd)
            if keyref_info:
                st.write("Keyref Elements:")
                for keyref in keyref_info:
                    st.write(keyref)

            # Generate the XML document.
            generated_xml = xsd.tostring()

            # Display the generated XML using Streamlit markdown.
            st.write("### Generated XML")
            st.code(generated_xml, language="xml")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == '__main__':
    main()
