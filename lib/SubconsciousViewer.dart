
import 'package:flutter/material.dart';

class SubconsciousViewer extends StatelessWidget {
  final Map<String, Map<String, int>> subconsciousData = {
    "TestProject": {
      "Summarizer": 4,
      "PDFParser": 2,
      "Uploader": 3
    },
    "AnotherProject": {
      "LoginAgent": 1,
      "ProfileUpdater": 2
    }
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("🧠 Subconscious Memory")),
      body: ListView(
        children: subconsciousData.entries.map((project) {
          return ExpansionTile(
            title: Text(project.key),
            children: project.value.entries.map((entry) {
              return ListTile(
                title: Text(entry.key),
                trailing: Text("used ${entry.value}x"),
              );
            }).toList(),
          );
        }).toList(),
      ),
    );
  }
}
