# Text_Segmentaion
Structured data extraction from unstructured text based on law documents

The main goal of the project is to extract/divide law documents into sections like 
```python
["Defined Terms", "Term of Agreement", "Company's Covenants Summarized", "The Executive's Covenants", "Certain Compensation Other Than Severance Payments"]
```

We do it by parsing documents and creating structure of the lists, bacause based on the data in 90% Sections names is used in numeration lists.
We create for each list regex rules and based on this we create nested list structure.
Main list will be at 0 level of the list nesting.

Data is taken from [lawinsider.com](https://www.lawinsider.com/)
