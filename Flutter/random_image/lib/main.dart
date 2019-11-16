//This is a random image generator because that is fun!

import 'package:flutter/material.dart';
import 'package:random_color/random_color.dart';

void FlatButton() {}

void main() {
  runApp(
    MaterialApp(
      home: Scaffold(
        backgroundColor: Colors.blueGrey[900],
        appBar: AppBar(
          title: Center(
            child: Text("Random Image"),
          ),
          //Seems like a random color generator should also have a random Hue
          backgroundColor: RandomColor().randomColor(colorHue: ColorHue.blue),
        ),
        body: Center(
          child: Image.network('https://picsum.photos/500/500'),
        ),
      ),
    ),
  );
}
