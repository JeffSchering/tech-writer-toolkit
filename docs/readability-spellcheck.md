# Spell check a text document

Use the SpellCheck class in the toolkit to check spelling of plain text content.

The class has a constructor and two methods:

<dl>
    <dt>constructor</dt>
    <dd>The constructor takes one optional parameter: the name of the file that contains the word list. The default name is <i>spell</i>.</dd>
    <dt>check_spelling(text)</dt>
    <dd>The <i>text</i> parameter is a UTF-8 encoded string. The method returns a dict where the key is the misspelled word and the value is the word number in the text. For example: <code>{'govermint': 12, 'livr': 27 }</code>. The count is one-based, not zero-based.<dd>
    <dt>add_word(word)</dt>
    <dd>Adds a word to the end of the spell file.</dd>
</dl>

A misspelled word is defined as any string of characters that isn't in the word list file.

## The word list

By default, the list of words is in the file *spell*. Because the file is UTF-8 encoded, it can have words such as Привет and 你好.

The file is very simple: One word per line. The file does not need to be sorted, but you might want to sort it for testing and debugging.

The file that comes with the toolkit is currently very small. If you want a decent list of words, you have to build it yourself.

You can use a custom file by setting the file parameter when you create the SpellCheck object. The file must exist, otherwise an exception is thrown. For example, to spell check a French text, create a word list file that contains French words. You can use any name for the file that you want, but *spell_fr* might be a good one. In that case, you would create the SpellCheck object like this, assuming that *spell_fr* is in the current directory:

```python
sc = SpellCheck('spell_fr')
```

Currently only one file per object can be used, but you can get around that limitation by creating an empty file, then appending the base file and your custom file. Your program can do this at runtime or you can prepare it in advance.

