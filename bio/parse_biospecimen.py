#!/usr/bin/python

import sys
from lxml import etree
import re
import json

# TCGA files have many namespaces, we need to get all of them correctly
def parse_biospecimen(biospecimen_file)
   tree = etree.parse(biospecimen_file)
   root = tree.getroot() #this is the root; we can use it to find elements
   aliquots = root.findall('.//bio:aliquot', namespaces=root.nsmap) 
   blank_elements = re.compile("^\\n\s*$")
   
   #----------------------------------------------------------
   # tcga data is divided into admin and patient blocks
   # We are getting the admin elements here
   # TODO We are presently getting only first level elements
   # We need to decide if we need to get the lower level elements
   #----------------------------------------------------------
   admin_elements = {}
   # get admin block elements
   admin_element = root.find('.//admin:admin', namespaces=root.nsmap)
   for child in admin_element:
      admin_elements[child.tag.split("}")[1]] = child.text
   
   #-----------------------------------------------------------
   # Get aliquot elements. To parse we are going directly to the 
   #  aliqout block and then getting the parent of the block and 
   #     looping backwards. 
   #-----------------------------------------------------------
   # got to aliquot level and loop back
   for aliquot in aliquots:
      aliquot_elements = {}
      biospecimen_elements = {}
      basic_element = aliquot
      # get aliquot elements
      # dive directly to the aliquots block and then loop back
      while True:
   
         # check if it is an element
         if not etree.iselement(basic_element):
           break
      
         # get all the elements in that particular block
         for child in basic_element:
            #just get the first level ( 1 level deep)
            if blank_elements.match(str(child.text)):
               continue
     
            # hash the data 
            element_name = child.tag.split("}")[1]
            element_text = child.text
      
            # collect aliquot details first/ do not replace
            if element_name not in aliquot_elements:
               aliquot_elements[element_name] = element_text
   
         parent = basic_element.getparent()
         basic_element = parent
         
         # loop back only till the tcga_bcr block
         if 'tcga_bcr' in parent.tag:
            break
      
      # json dump
      biospecimen_elements = dict(list(aliquot_elements.items()) + list(admin_elements.items())) 
      print json.dumps(biospecimen_elements)


