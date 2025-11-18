# User Manual - Grammar Analyzer

## Project Information

### Developed by:
- **David Leonardo Espíndola Núñez** - Code. 202128390  
- **Juan David Lopez Castro** - Code. 202023451  

#### Universidad Pedagógica y Tecnológica de Colombia  
###### Faculty of Engineering  
###### Systems and Computer Engineering  
---

## Starting the Analyzer

### Running the Program
1. Run the `main.py` file  
2. Main interface with function menu  
3. Grammar status indicator at the center  
4. Operation buttons for grammar manipulation  

## Defining a Grammar

### Creating a New Grammar

**Define Grammar:**
1. Click "📝 Definir Nueva Gramática"  
2. Enter non-terminals separated by commas (e.g., S,A,B)  
3. Enter terminals separated by commas (e.g., a,b)  
4. Specify the start symbol (must be a non-terminal)  

### Adding Productions

**Create productions:**
1. In the production section, enter the left side (e.g., S)  
2. Enter the right side (e.g., aSb)  
3. Click "Agregar" or press Enter  
4. Use 'ε' for empty productions  
5. Productions are displayed in the format: `S → aSb | ab`  

**Remove productions:**
- Click "Eliminar Última" to remove the last added production  

**Complete grammar creation:**
- Click "Crear Gramática" when all productions are defined  
- The system automatically classifies the grammar type  

### Grammar Types

The analyzer automatically classifies grammars according to Chomsky Hierarchy:

**Type 3 (Regular):**
- Productions: A → aB, A → a, A → ε  
- Example: S → aS | ε  

**Type 2 (Context-Free):**
- Left side: single non-terminal  
- Example: S → aSb | ab  

**Type 1 (Context-Sensitive):**
- Restriction: |α| ≤ |β| (except S→ε)  
- Example: S → aSBC | aBC, CB → BC  

**Type 0 (Unrestricted):**
- No restrictions on productions  

## Loading and Saving

### Save Grammar
1. Click "💾 Guardar Gramática"  
2. Choose location and filename  
3. Saved in JSON format with complete information  

### Load Grammar
1. Click "📂 Cargar Gramática"  
2. Select JSON file  
3. Grammar is loaded and automatically classified  

### JSON Format
```json
{
  "nonterminals": ["S", "A"],
  "terminals": ["a", "b"],
  "productions": {
    "S": ["aSb", "ab"]
  },
  "start_symbol": "S",
  "type": 2
}
```

## Grammar Analysis

### View Information

**Grammar details:**
1. Click "ℹ️ Mostrar Información"  
2. Displays complete quintuple:
   - Non-terminals (N)
   - Terminals (T)
   - Start symbol (S)
   - Productions (P)
   - Grammar type classification  

### Syntax Tree

**View production structure:**
1. Click "🌳 Árbol de Síntesis"  
2. Shows hierarchical tree of productions  
3. Displays recursive references  
4. Identifies terminal and non-terminal symbols  

## String Evaluation

### Evaluating Strings

**Parse string:**
1. Click "✓ Evaluar Cadena"  
2. Enter the string to evaluate  
3. Use 'ε' for empty string  
4. Click "Evaluar" or press Enter  

### Evaluation Results

**Accepted string:**
- Shows "✓ CADENA ACEPTADA"  
- Displays step-by-step derivation tree  
- Shows applied productions in sequence  

**Rejected string:**
- Shows "✗ CADENA RECHAZADA"  
- Indicates the string does not belong to the language  

### Parsing Algorithms

The analyzer uses different algorithms depending on grammar type:

**Type 3 (Regular):**
- BFS algorithm over finite automaton states  
- Very efficient for regular languages  

**Type 2 (Context-Free):**
- BFS over sentential forms  
- Expands leftmost non-terminal first  

**Type 0/1 (General):**
- Exhaustive search with backtracking  
- Applies all possible productions  

## Language Generation

### Generating Strings

**Generate shortest strings:**
1. Click "📤 Generar Cadenas"  
2. Enter quantity (default: 10)  
3. Click "Generar"  

### Generation Results

**Output display:**
- Lists generated strings ordered by length  
- Shows string length for each  
- Format: `1. 'ab' (longitud: 2)`  

**Generation algorithm:**
- Uses BFS to explore derivations  
- Collects only terminal forms  
- Sorts by increasing length  

## System Validations

### Automatic Checks

**Grammar definition:**
- At least one non-terminal must exist  
- At least one terminal must exist  
- Start symbol must be a non-terminal  
- At least one production must be defined  

**String evaluation:**
- Grammar must be defined before evaluation  
- Symbols must belong to the alphabet  

### Error Messages
- "Debe definir al menos un no terminal"  
- "El símbolo inicial debe estar en los no terminales"  
- "Debe definir al menos una producción"  
- "Primero debe definir o cargar una gramática"  

## Grammar Examples

### Type 3 - Language a*b*
```
Non-terminals: S,A
Terminals: a,b
Start: S

Productions:
S → aS | A | ε
A → bA | ε
```

### Type 2 - Language aⁿbⁿ
```
Non-terminals: S
Terminals: a,b
Start: S

Productions:
S → aSb | ab
```

### Type 2 - Palindromes
```
Non-terminals: S
Terminals: a,b
Start: S

Productions:
S → aSa | bSb | a | b | ε
```

### Type 2 - Arithmetic Expressions
```
Non-terminals: E,T,F
Terminals: +,*,(,),id
Start: E

Productions:
E → E + T | T
T → T * F | F
F → ( E ) | id
```

### Type 1 - Language aⁿbⁿcⁿ
```
Non-terminals: S,A,B,C
Terminals: a,b,c
Start: S

Productions:
S → aSBC | aBC
CB → BC
aB → ab
bB → bb
bC → bc
cC → cc
```

## Visual Indicators

### Status Display

**Grammar not loaded:**
- Red text: "No hay gramática cargada"  

**Grammar loaded:**
- Green text: "✓ Tipo X (Nombre del tipo)"  
- Shows current grammar classification  

### Window Titles

- Main window: "Analizador Universal de Gramáticas Formales"  
- Define dialog: "Definir Gramática"  
- Info window: "Información de la Gramática"  
- Evaluation: "Resultado de Evaluación"  
- Generation: "Cadenas Generadas"  

## Technical Limitations

### Performance Limits
- Type 3 parsing: 10,000 max steps  
- Type 2 parsing: 5,000 max steps  
- General parsing: 1,000 max steps  
- Generated strings: maximum 20 characters  

### Supported Features
- Grammar types: 0, 1, 2, and 3  
- Symbol format: single characters or multi-character strings  
- Epsilon symbol: ε (epsilon)  
- Platform: Python 3.8+  

### Known Limitations
- Finds ONE derivation (not all for ambiguous grammars)  
- Type 0/1 parsing can be slow for complex grammars  
- Very long derivations may exceed display limits  

## Troubleshooting

### Technical Issues

**Program won't start:**
- Check Python 3.8+ installation  
- Verify tkinter: `python -m tkinter`  
- Check all module files are present  

**Buttons not responding:**
- Restart the program  
- Verify grammar is loaded for evaluation/generation  

**JSON loading error:**
- Verify valid JSON syntax  
- Check all required fields exist  
- Ensure productions reference valid symbols  

### Usage Issues

**Grammar not accepting expected strings:**
- Verify start symbol is correct  
- Check all necessary productions are defined  
- Use "Mostrar Información" to review grammar  
- Test with "Generar Cadenas" to see what it produces  

**String evaluation too slow:**
- Grammar may be too complex for its type  
- Try simplifying productions  
- Type 0/1 grammars are inherently slower  

**Generation produces unexpected strings:**
- Verify terminals and non-terminals are correctly defined  
- Check for unintended epsilon productions  
- Review production rules carefully  

**Cannot add production:**
- Verify left side is not empty  
- Check symbols are properly formatted  
- Ensure epsilon is typed as 'ε' not 'e'  

## Advanced Usage

### Testing Grammar Completeness

1. Generate strings to see what the grammar produces  
2. Evaluate known valid strings  
3. Evaluate known invalid strings  
4. Review the syntax tree for recursive patterns  

### Debugging Grammars

**Grammar too restrictive:**
- Add alternative productions  
- Check for missing base cases  

**Grammar too permissive:**
- Remove or restrict productions  
- Add context to productions (Type 1)  

### Converting Between Types

**Regular to CFG:**
- Already compatible (Type 3 ⊂ Type 2)  
- No conversion needed  

**CFG to Regular:**
- Only possible if language is regular  
- Check if right-linear or left-linear form exists  

## Best Practices

### Grammar Design
- Start with simple productions and test  
- Use meaningful non-terminal names  
- Document complex productions  
- Test incrementally as you add rules  

### Testing Strategy
1. Define grammar  
2. Generate strings to verify  
3. Test boundary cases (empty string, single char)  
4. Test expected accepts and rejects  
5. Review derivation trees for correctness  

### Performance Optimization
- Keep Type 2 grammars unambiguous when possible  
- Limit production chain length  
- Avoid unnecessary epsilon productions  
- Use Type 3 when the language is regular  

---

**Universal Formal Grammar Analyzer** - Educational Tool for Formal Language Theory
