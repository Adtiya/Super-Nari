
import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Love Feature')),
        body: Center(child: LoveWidget()),
      ),
    );
  }
}

class LoveWidget extends StatefulWidget {
  @override
  _LoveWidgetState createState() => _LoveWidgetState();
}

class _LoveWidgetState extends State<LoveWidget> {
  bool isLoved = false;

  void _toggleLove() {
    setState(() {
      isLoved = !isLoved;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        IconButton(
          onPressed: _toggleLove,
          color: isLoved ? Colors.red : Colors.grey,
          icon: Icon(isLoved ? Icons.favorite : Icons.favorite_border),
          iconSize: 100.0,
        ),
        Text(
          isLoved ? "You loved this" : "Press the heart to love",
          style: TextStyle(fontSize: 24.0),
        ),
      ],
    );
  }
}
