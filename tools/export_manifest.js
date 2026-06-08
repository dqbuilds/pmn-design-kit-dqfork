/*
 * export_manifest.js — Figma → manifest exporter (the Figma→code loop)
 * =====================================================================
 * Reads a PMN template component in Figma and emits its manifest JSON
 * (templates/<name>.manifest.json). The manifest is GENERATED from Figma —
 * never hand-edited. This is what makes "edit the template in Figma" update
 * the code: change the component, re-run this, commit the regenerated manifest.
 *
 * What it extracts, all from Figma:
 *   - structure: every slot node named '#...' (text) or '@...' (geometry/bar)
 *   - semantics: each slot's data binding, read from shared plugin data
 *     (namespace 'pmn': keys bind / kind / format / transform / reflow / scale).
 *     Annotate slots once in Figma; the binding then lives in the file.
 *   - token bindings: the color variable each slot's fill is bound to, and the
 *     font-family variable — read live, so retheming is captured automatically.
 *   - lists: any frame annotated pmn:list=<path> is emitted as a repeating list,
 *     with its row component + the row's inner slots (variable-length cards).
 *   - brand: the Brand collection + its modes (the reskin mechanism).
 *   - field: the code-set gradient node (gradient stops can't bind to variables).
 *
 * HOW TO RUN (on-demand / agent-triggered, matching the chosen automation level):
 *   Paste this whole file into a `use_figma` call, then append:
 *       const FK = "<fileKey>";
 *       return await exportManifest("<componentNodeId>", "<template-name>", FK);
 *   Write the returned JSON to templates/<template-name>.manifest.json.
 *
 * A pure visual edit in Figma needs no re-export. Re-export only when the
 * CONTRACT changes: a slot added / renamed / removed, a token rebinding, a new
 * brand mode, or a new list.
 */
async function exportManifest(componentId, templateName, fileKey) {
  const comp = await figma.getNodeByIdAsync(componentId);
  const byId = {};
  for (const v of await figma.variables.getLocalVariablesAsync()) byId[v.id] = v.name;
  const vn = (id) => (id ? byId[id] || null : null);
  const insideInstance = (n) => { let p = n.parent; while (p) { if (p.type === "INSTANCE") return true; p = p.parent; } return false; };
  const fillVar = (n) => vn(n.fills && n.fills[0] && n.fills[0].boundVariables && n.fills[0].boundVariables.color && n.fills[0].boundVariables.color.id);
  const fontVar = (n) => vn(n.boundVariables && n.boundVariables.fontFamily && n.boundVariables.fontFamily.id);
  const sd = (n, k) => { const v = n.getSharedPluginData("pmn", k); return v || undefined; };

  function slotOf(n) {
    const o = { name: n.name, kind: sd(n, "kind") || (n.name.startsWith("@") ? "bar" : "text") };
    for (const k of ["bind", "format", "transform", "scale"]) { const v = sd(n, k); if (v) o[k] = v; }
    if (sd(n, "reflow") === "true") o.reflow = true;
    const fv = fillVar(n); if (fv) o.token = fv;
    const ff = fontVar(n); if (ff) o.font = ff;
    return o;
  }

  const slots = comp
    .findAll((n) => (n.name.startsWith("#") || n.name.startsWith("@")) && !insideInstance(n))
    .map(slotOf);

  const lists = [];
  for (const ln of comp.findAll((n) => sd(n, "list"))) {
    const inst = ln.children.find((c) => c.type === "INSTANCE");
    let item = null;
    if (inst) {
      const main = await inst.getMainComponentAsync();
      item = {
        component: main ? main.name : null,
        slots: inst.findAll((c) => c.name.startsWith("#") || c.name.startsWith("@")).map(slotOf),
      };
    }
    lists.push({ node: ln.name, bind: sd(ln, "list"), item });
  }

  const fieldNode = comp.findOne((n) => n.name === "field");
  const cols = await figma.variables.getLocalVariableCollectionsAsync();
  const brand = cols.find((c) => c.name === "Brand");

  const m = {
    template: templateName,
    version: "0.2",
    _generated: "by tools/export_manifest.js from Figma — do not hand-edit",
    figma: { fileKey, componentName: comp.name, componentNodeId: comp.id, canvas: [comp.width, comp.height], autolayout: true },
    brand: brand ? { collection: "Brand", modes: brand.modes.map((x) => x.name), mechanism: "setExplicitVariableModeForCollection" } : null,
    field: fieldNode ? { node: "field", kind: "gradient", codeSet: true, stops: ["color/field/start", "color/field/mid", "color/field/end"] } : null,
    slots,
  };
  if (lists.length) m.lists = lists;
  return m;
}
