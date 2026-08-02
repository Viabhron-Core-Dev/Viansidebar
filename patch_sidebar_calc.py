with open("app/src/main/java/com/example/service/CalculatorPageView.kt", "r") as f:
    content = f.read()

content = content.replace("getChildAt(0).findViewById<TableLayout>(getChildAt(0).id)", "findViewById(R.id.tableLayout)")
content = content.replace("val tableLayout = findViewById<TableLayout>(R.id.tableLayout) ?: findViewById(R.id.tableLayout)", "val tableLayout = findViewById<TableLayout>(R.id.tableLayout)")

# Actually, the ID in XML is empty for TableLayout. Let's patch XML to add the id, or just find it by traversing
with open("app/src/main/res/layout/page_calculator.xml", "r") as f:
    xml_content = f.read()

xml_content = xml_content.replace("<TableLayout", "<TableLayout android:id=\"@+id/tableLayout\"")

with open("app/src/main/res/layout/page_calculator.xml", "w") as f:
    f.write(xml_content)

with open("app/src/main/java/com/example/service/CalculatorPageView.kt", "w") as f:
    f.write(content)
