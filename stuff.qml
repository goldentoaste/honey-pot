import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    width: 820
    height: 480
    visible: true
    title: qsTr("Qt Markdown Example by Raymii.org")

    QtObject{
        id: markdown
        // not having tabs or spaces is important, otherwise
        // the markdown will not render.
        property string text: "*Italic*    **Bold**

# Heading 1

## Heading 2

[Link to raymii.org](https://raymii.org)


> quote

* List
* List

1. list 2
1. list 2

```
Code()->example
```

First Header | Second Header
------------ | -------------
Content from cell 1 | Content from cell 2
Content in the first column | Content in the second column

    "}

    Text {
        id: textedittext
        text: "QML TextEdit{}:"
        anchors.top: parent.top
        anchors.left: parent.left
    }

    Rectangle {
        id: textedit
        anchors.top: textedittext.bottom
        anchors.left: parent.left
        anchors.topMargin: 20
        anchors.leftMargin: 5
        width: 400
        height: 400
        border.color: "lime"

        TextEdit{
            anchors.fill: parent
            textMargin: 5
            textFormat: TextEdit.MarkdownText
            text: markdown.text
            wrapMode: Text.Wrap
        }
    }

    Text {
        id: texttext
        text: "QML Text{}:"
        anchors.top: parent.top
        anchors.left: textedit.right
    }

    Rectangle {
        id: text
        anchors.top: texttext.bottom
        anchors.left: textedit.right
        anchors.topMargin: 20
        anchors.leftMargin: 5
        width: 400
        height: 400
        border.color: "teal"


        Text{
            anchors.fill: parent
            textFormat: TextEdit.MarkdownText
            text: markdown.text
            fontSizeMode: Text.Fit
            wrapMode: Text.WordWrap
        }
    }
}