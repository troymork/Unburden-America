# Notion Import Guide

This folder contains CSVs and a suggested property schema for three databases that mirror your workbook.

## Databases
1. **Project Overview** → `Project_Overview.csv`
2. **Milestones** → `Milestones.csv`
3. **Project Needs** → `Project_Needs.csv`

## Import Steps
1. In Notion… create a new database for each CSV.
2. Use **“Merge with CSV”** or **“Create from CSV”** and select the corresponding file.
3. Ensure the **first column** is mapped to the **Title** property.
4. Use `notion_schemas.json` as a guide to set property types… adjust as needed.
5. Set Relations:  
   • `Milestones.Project` → relation to **Project Overview**  
   • `Project Needs.Project` → relation to **Project Overview**

## Suggested Views
- **Milestones**: Board by Status… Calendar by Due Date… Table by Owner.
- **Project Needs**: Board by Priority… Table with Budget… List by Category.
- **Project Overview**: Gallery with hero summary… Table with KPIs and Budgets.
