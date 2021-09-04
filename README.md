# Real-Time Localization System (RTLS) Integration with Building Information Modeling (BIM)
The main modules of the integration system include (I) Retriveing physical context infromation from the BIM model; (II) Detecting the presence of the target node in the desired workspaces on-site

### Module (I): Retriveing Physical Context Infromation From the BIM Model
The BIM model includes the complete geometrical description of the building, and it was developed by Autodesk’s Revit version 2020. The user can generate workspaces and danger zones as 2D spaces and specify their type in the element properties. Dynamo scripting language was used to retrieve the identification of the spaces and generate Comma-Separated Values (CSV) file containing spaces information. The extracted features for each element are element ID, family type, type and (x,y) coordinates of vertices composing the bounding edges.

### Module (II): Detecting the Presence of the Target Node in the Desired Workspaces
Wooff’s Algorithm is deployed to determine whether the target node lies inside a workspace. It uses the property that the summation of all angles created between lines connecting the location of the worker point P and the ith and (i + 1)th vertices of a given workspace equals zero if point P lies outside the workspace and equals to ± 2π if point P lies inside the workspace.
