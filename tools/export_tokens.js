/*
 * export_tokens.js — Figma variables → tokens.json (the token round-trip)
 * =======================================================================
 * Dumps every PMN design token (the `Brand` collection — one mode per brand —
 * plus the `Layout` collection) to JSON so the CODE SIDE TRACKS what designers
 * change in Figma. Brands live as MODES of the Brand collection: editing a
 * color in the Variables panel (or adding a sub-brand mode) and re-running this
 * keeps templates/tokens.json in sync. Same "Figma is the source of truth,
 * code holds a generated mirror" pattern as export_manifest.js.
 *
 * The emitted tokens.json is consumed by the render/orchestration layer and is
 * the canonical reference for brand palettes (each mode = a brand package).
 *
 * HOW TO RUN (on-demand / agent-triggered):
 *   Paste this whole file into a `use_figma` call, then append:
 *       return await exportTokens();
 *   Write the returned JSON to templates/tokens.json. Commit it.
 *
 * Re-run whenever a token value changes, a scope/code-syntax changes, or a
 * brand (mode) is added. A pure rename of a brand mode also warrants a re-run.
 */
async function exportTokens() {
  const hex = (c) => {
    const h = (x) => Math.round(Math.max(0, Math.min(1, x)) * 255).toString(16).padStart(2, "0");
    const base = `#${h(c.r)}${h(c.g)}${h(c.b)}`;
    return c.a != null && c.a < 1 ? base + h(c.a) : base;
  };
  const colls = await figma.variables.getLocalVariableCollectionsAsync();
  const allVars = await figma.variables.getLocalVariablesAsync();
  const out = { _generated: "by tools/export_tokens.js from Figma — do not hand-edit", collections: {} };

  for (const coll of colls) {
    if (!["Brand", "Layout"].includes(coll.name)) continue;
    const modeNames = {}; coll.modes.forEach((m) => (modeNames[m.modeId] = m.name));
    const entry = {
      modes: coll.modes.map((m) => m.name),
      isBrand: coll.name === "Brand",
      tokens: {},
    };
    for (const v of allVars.filter((v) => v.variableCollectionId === coll.id)) {
      const values = {};
      for (const [mid, val] of Object.entries(v.valuesByMode)) {
        let out2 = val;
        if (v.resolvedType === "COLOR" && val && typeof val === "object" && "r" in val) out2 = hex(val);
        else if (val && val.type === "VARIABLE_ALIAS") out2 = { alias: val.id };
        values[modeNames[mid]] = out2;
      }
      entry.tokens[v.name] = {
        type: v.resolvedType,
        scopes: v.scopes,
        code: v.codeSyntax || {},
        values,
      };
    }
    out.collections[coll.name] = entry;
  }
  return out;
}
