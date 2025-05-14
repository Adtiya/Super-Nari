
import 'package:flutter/material.dart';
import 'FeatureTab.dart';
import 'DeployTab.dart';
import 'ManageFeaturesTab.dart';
import 'NewProjectTab.dart';
import 'SmartDashboardTab.dart';
import 'ASIDashboardTab.dart';
import 'MemoryTab.dart';
import 'AgentBuilderTab.dart';
import 'SuperAgentBuilderTab.dart';
import 'HealingAgentTab.dart';
import 'MemoryTimelineTab.dart';
import 'AgentTemplatesTab.dart';
import 'SubconsciousViewer.dart';

void main() {
  runApp(SuperNariFullApp());
}

class SuperNariFullApp extends StatefulWidget {
  @override
  _SuperNariFullAppState createState() => _SuperNariFullAppState();
}

class _SuperNariFullAppState extends State<SuperNariFullApp> {
  ThemeMode _themeMode = ThemeMode.dark;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Super NARI Full Stack',
      themeMode: _themeMode,
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF121212),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.grey[900],
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blueAccent,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            textStyle: TextStyle(fontSize: 16),
          ),
        ),
      ),
      home: DashboardHome(toggleTheme: () {
        setState(() {
          _themeMode = _themeMode == ThemeMode.dark ? ThemeMode.light : ThemeMode.dark;
        });
      }),
    );
  }
}

class DashboardHome extends StatefulWidget {
  final VoidCallback toggleTheme;

  DashboardHome({required this.toggleTheme});

  @override
  _DashboardHomeState createState() => _DashboardHomeState();
}

class _DashboardHomeState extends State<DashboardHome> with SingleTickerProviderStateMixin {
  late TabController tabController;
  final tabs = [
    'Memory',
    'Smart Dashboard',
    'Super Agents',
    'Agents',
    'ASI',
    'New Project',
    'Build',
    'Deploy',
    'Manage',
    'Healing Agent',
    'Subconscious'
  ];

  @override
  void initState() {
    super.initState();
    tabController = TabController(length: tabs.length, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('🧠 Super NARI Full Stack'),
        centerTitle: true,
        backgroundColor: Theme.of(context).appBarTheme.backgroundColor,
        actions: [
          IconButton(
            icon: Icon(Icons.brightness_6),
            onPressed: widget.toggleTheme,
            tooltip: "Toggle Theme",
          )
        ],
        bottom: TabBar(
          controller: tabController,
          isScrollable: true,
          indicatorColor: Colors.blueAccent,
          tabs: tabs.map((tab) => Tab(text: tab)).toList(),
        ),
      ),
      body: TabBarView(
        controller: tabController,
        children: [
          MemoryTab(),
          SmartDashboardTab(),
          SuperAgentBuilderTab(),
          AgentBuilderTab(),
          ASIDashboardTab(),
          NewProjectTab(),
          FeatureTab(),
          DeployTab(),
          ManageFeaturesTab(),
          HealingAgentTab(),
	  SubconsciousViewer(), 
        ],
      ),
    );
  }
}
