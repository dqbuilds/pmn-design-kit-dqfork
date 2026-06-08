/*
 * export_manifest.js — Figma → manifest exporter (the Figma→code loop)
 * =====================================================================
 * Reads a PMN template component in Figma and emits its manifest JSON
 * (templates/<name>.manifest.json). The manifest is GENERATED from Figma —
 * never hand-edited. Change the component, re-run this, commit the manifest.
 *
 * v3 architecture notes:
 *   - Shared chrome (Header/Footer) and the Background are NESTED component
 *     instances tagged pmn:role = chrome|background|showmark. Their slots
 *     (#logo.*, #source, @bg.image) must still be captured, so those instances
 *     are treated as TRANSPARENT: the walk descends through them. Any OTHER
 *     nested instance is opaque (its interior is that component's own content).
 *   - Lists declare their row component by name in pmn:list-item (no longer
 *     inferred from an example instance), so example rows can be detached frames
 *     (needed because instance bars can't be resized). Row slots are read from
 *     the row COMPONENT on the current page.
 *   - The field gradient binds to color/field/* variables (reskins via the brand
 *     mode), so there is no code-set "field" node → manifest.field is null.
 *
 * HOW TO RUN (on-demand / agent-triggered):
 *   Paste this whole file into a `use_figma` call, then append:
 *       const FK = "<fileKey>";
 *       await figma.setCurrentPageAsync(<page containing the components>);
 *       return await exportManifest("<componentNodeId>", "<template-name>", FK);
 *   Write the returned JSON to templates/<template-name>.manifest.json.
 */
async function exportManifest(componentId, templateName, fileKey) {
  const comp = await figma.getNodeByIdAsync(componentId);
  const byId = {};
  for (const v of await figma.variables.getLocalVariablesAsync()) byId[v.id] = v.name;
  const vn = (id) => (id ? byId[id] || null : null);
  const TRANSPARENT = ["chrome", "background", "showmark"];
  // A node is BLOCKED only if it sits inside a non-transparent instance.
  const blockedByInstance = (n) => {
    let p = n.parent;
    while (p) {
      if (p.type === "INSTANCE" && !TRANSPARENT.includes(p.getSharedPluginData("pmn", "role"))) return true;
      p = p.parent;
    }
    return false;
  };
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

  // exclude nodes inside a list (the list path captures those) and any node that
  // is itself a role marker (e.g. the showmark wordmark group is static, not a slot)
  const insideList = (n) => { let p = n.parent; while (p && p.id !== comp.id) { if (p.getSharedPluginData && p.getSharedPluginData("pmn", "list")) return true; p = p.parent; } return false; };
  const slots = comp
    .findAll((n) => (n.name.startsWith("#") || n.name.startsWith("@")) && !blockedByInstance(n) && !insideList(n) && !sd(n, "role"))
    .map(slotOf);

  const lists = [];
  for (const ln of comp.findAll((n) => sd(n, "list"))) {
    let item = null;
    const compName = sd(ln, "list-item");
    if (compName) {
      const rowComp = figma.currentPage.findOne((n) => n.type === "COMPONENT" && n.name === compName);
      item = {
        component: compName,
        slots: rowComp ? rowComp.findAll((c) => c.name.startsWith("#") || c.name.startsWith("@")).map(slotOf) : [],
      };
    } else {
      // legacy fallback: infer row component from an example instance child
      const inst = ln.children.find((c) => c.type === "INSTANCE");
      if (inst) {
        const main = await inst.getMainComponentAsync();
        item = { component: main ? main.name : null, slots: inst.findAll((c) => c.name.startsWith("#") || c.name.startsWith("@")).map(slotOf) };
      }
    }
    lists.push({ node: ln.name, bind: sd(ln, "list"), item });
  }

  // v3: field is a Background component instance with variable-bound gradient
  // stops (reskins via mode). A legacy code-set node literally named "field"
  // is still emitted if present.
  const fieldNode = comp.findOne((n) => n.name === "field");
  const cols = await figma.variables.getLocalVariableCollectionsAsync();
  const brand = cols.find((c) => c.name === "Brand");

  const m = {
    template: templateName,
    version: "0.3",
    _generated: "by tools/export_manifest.js from Figma — do not hand-edit",
    figma: { fileKey, componentName: comp.name, componentNodeId: comp.id, canvas: [comp.width, comp.height], autolayout: true },
    brand: brand ? { collection: "Brand", modes: brand.modes.map((x) => x.name), mechanism: "setExplicitVariableModeForCollection" } : null,
    field: fieldNode ? { node: "field", kind: "gradient", codeSet: true, stops: ["color/field/start", "color/field/mid", "color/field/end"] } : null,
    slots,
  };
  if (lists.length) m.lists = lists;
  return m;
}
