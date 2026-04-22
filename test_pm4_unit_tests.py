"""
AI-GENERATED TESTS (Course AI Policy)

Prompt used:
"Create a Python unit test file for PM4 functions implemented in index.html.
Use unittest, include at least one unit test per selected implemented function,
and at least one integration test across multiple functions. The file must contain
only tests, and tests should be runnable in terminal with easily verifiable output."

Prompt used:
"Build tests that execute the real JavaScript from index.html by extracting the
<script> block and evaluating it in Node with lightweight DOM/localStorage stubs,
then assert behavior for: getDisplayCommonNames, setSelectedSuggestion,
resetAnalysisState, startNewEntry, plus one integration workflow test."
"""

import subprocess
import textwrap
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INDEX_HTML = ROOT / "index.html"


def run_js_assertions(assertion_js: str) -> subprocess.CompletedProcess:
    assertion_json = json.dumps(assertion_js)
    harness = textwrap.dedent(
        f"""
        const fs = require('fs');

        const html = fs.readFileSync({INDEX_HTML.as_posix()!r}, 'utf8');
        const m = html.match(/<script>([\\s\\S]*?)<\\/script>/i);
        if (!m) {{
          console.error('Could not find script block in index.html');
          process.exit(1);
        }}

        function makeElement() {{
          return {{
            value: '',
            textContent: '',
            innerHTML: '',
            className: '',
            checked: false,
            style: {{}},
            addEventListener() {{}},
            appendChild() {{}},
            append() {{}},
            setAttribute() {{}},
            querySelector() {{
              return {{ addEventListener() {{}}, classList: {{ add() {{}}, remove() {{}}, toggle() {{}} }} }};
            }},
            classList: {{
              add() {{}},
              remove() {{}},
              toggle() {{}}
            }}
          }};
        }}

        const ids = [
          'dateField', 'journalName', 'locationField', 'notes', 'photoInput',
          'addPhotoBtn', 'photoList', 'locationToggle', 'locationState',
          'saveBtn', 'undoBtn', 'resetBtn', 'exportBtn', 'status', 'entryMeta',
          'analysisState', 'analysisBanner', 'selectedMatch', 'matches',
          'collectionsBtn', 'addNewEntryBtn', 'backToLogBtn', 'logPage',
          'collectionsPage', 'collectionList'
        ];
        const map = Object.fromEntries(ids.map((id) => [id, makeElement()]));

        global.document = {{
          getElementById(id) {{
            if (!map[id]) map[id] = makeElement();
            return map[id];
          }},
          createElement() {{
            const el = makeElement();
            el.firstElementChild = makeElement();
            return el;
          }}
        }};

        global.window = {{ addEventListener() {{}} }};
        global.location = {{ hash: '', host: '127.0.0.1:8000' }};
        global.navigator = {{}};

        const storage = {{}};
        global.localStorage = {{
          _removed: [],
          getItem(k) {{ return Object.prototype.hasOwnProperty.call(storage, k) ? storage[k] : null; }},
          setItem(k, v) {{ storage[k] = String(v); }},
          removeItem(k) {{ delete storage[k]; this._removed.push(k); }}
        }};

        global.fetch = async () => ({{ ok: true, json: async () => ({{ result: {{ classification: {{ suggestions: [] }} }} }}) }});
        global.URL = {{ createObjectURL() {{ return 'blob:test'; }} }};
        global.File = function(parts, opts) {{ this.parts = parts; this.opts = opts; }};

        const assert = (condition, message) => {{
          if (!condition) throw new Error(message);
        }};

        try {{
          const assertionCode = {assertion_json};
          eval(m[1] + '\\n' + assertionCode + '\\nconsole.log("JS_ASSERTIONS_OK")');
        }} catch (err) {{
          console.error(err && err.stack ? err.stack : String(err));
          process.exit(1);
        }}
        """
    )
    return subprocess.run(["node", "-e", harness], capture_output=True, text=True, cwd=ROOT)


class TestPM4Functions(unittest.TestCase):
    def test_getDisplayCommonNames_unit(self):
        js = textwrap.dedent(
            """
            assert(getDisplayCommonNames(['A', 'B']) === 'A, B', 'array names should join');
            assert(getDisplayCommonNames({ en: ['One', 'Two'] }) === 'One, Two', 'en array should join');
            assert(getDisplayCommonNames({ en: 'Solo' }) === 'Solo', 'en string should pass through');
            assert(getDisplayCommonNames(null) === 'No common names provided', 'null should fallback');
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    def test_setSelectedSuggestion_unit(self):
        js = textwrap.dedent(
            """
            state.analysis.suggestions = [
              { id: 'abc', name: 'Test Mushroom', probability: 0.72, details: { url: 'https://example.test' } }
            ];
            setSelectedSuggestion(0);
            assert(state.analysis.selectedIndex === 0, 'selected index should be 0');
            assert(state.analysis.selectedSuggestion.name === 'Test Mushroom', 'selected suggestion should be set');
            assert(state.entry.selectedSuggestion.name === 'Test Mushroom', 'entry selected suggestion should mirror');
            assert(state.entry.speciesId === 'abc', 'species id should come from selected suggestion');
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    def test_resetAnalysisState_unit(self):
        js = textwrap.dedent(
            """
            state.analysis = { status: 'done', error: 'x', suggestions: [{name:'x'}], selectedIndex: 2, selectedSuggestion: {name:'x'}, warning: 'warn' };
            state.entry.selectedSuggestion = { name: 'x' };
            state.entry.speciesId = 'abc';
            resetAnalysisState();
            assert(state.analysis.status === 'idle', 'status should reset to idle');
            assert(Array.isArray(state.analysis.suggestions) && state.analysis.suggestions.length === 0, 'suggestions should clear');
            assert(state.analysis.selectedIndex === -1, 'selected index should reset');
            assert(state.entry.selectedSuggestion === null, 'entry selected suggestion should clear');
            assert(state.entry.speciesId === 'mushroom-001', 'speciesId should reset to default');
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    def test_startNewEntry_unit(self):
        js = textwrap.dedent(
            """
            state.entry.savedId = 'keep-me';
            state.entry.savedAt = 'yesterday';
            state.entry.location = 'park';
            state.entry.notes = 'old note';
            state.entry.photos = [{ id: '1' }];
            state.entry.locationEnabled = true;
            state.entry.latitude = 10;
            state.entry.longitude = 20;
            state.entry.selectedSuggestion = { name: 'old' };
            state.entry.speciesId = 'old-species';

            let renderCalls = 0;
            const oldRender = render;
            render = function () {{ renderCalls += 1; }};

            startNewEntry();

            assert(state.entry.savedId === undefined, 'savedId should clear');
            assert(state.entry.savedAt === undefined, 'savedAt should clear');
            assert(state.entry.location === '', 'location should clear');
            assert(state.entry.notes === '', 'notes should clear');
            assert(Array.isArray(state.entry.photos) && state.entry.photos.length === 0, 'photos should clear');
            assert(state.entry.locationEnabled === false, 'location toggle should reset');
            assert(state.entry.latitude === null && state.entry.longitude === null, 'coordinates should reset');
            assert(state.entry.speciesId === 'mushroom-001', 'species id should reset');
            assert(localStorage._removed.includes('draft-entry-42'), 'draft key should be removed');
            assert(renderCalls === 1, 'render should run once');

            render = oldRender;
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    def test_integration_selection_then_new_entry_reset(self):
        js = textwrap.dedent(
            """
            state.analysis.suggestions = [
              { id: 'spec-1', name: 'Species One', probability: 0.9, details: { common_names: ['One'] } },
              { id: 'spec-2', name: 'Species Two', probability: 0.4, details: { common_names: ['Two'] } }
            ];

            setSelectedSuggestion(1);
            assert(state.entry.speciesId === 'spec-2', 'selection should update species id');
            assert(state.entry.selectedSuggestion && state.entry.selectedSuggestion.name === 'Species Two', 'selection should update entry selectedSuggestion');

            let renderCalls = 0;
            const oldRender = render;
            render = function () {{ renderCalls += 1; }};
            startNewEntry();

            assert(state.entry.speciesId === 'mushroom-001', 'new entry should reset species id');
            assert(state.entry.selectedSuggestion === null, 'new entry should clear selected suggestion');
            assert(state.analysis.selectedIndex === -1, 'analysis selected index should reset');
            assert(state.analysis.suggestions.length === 0, 'analysis suggestions should reset');
            assert(renderCalls === 1, 'integration should still render once');
            render = oldRender;
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    def test_integration_selection_then_new_entry_reset(self):
        js = textwrap.dedent(
            """
            state.analysis.suggestions = [
              { id: 'spec-1', name: 'Species One', probability: 0.9, details: { common_names: ['One'] } },
              { id: 'spec-2', name: 'Species Two', probability: 0.4, details: { common_names: ['Two'] } }
            ];

            setSelectedSuggestion(1);
            assert(state.entry.speciesId === 'spec-2', 'selection should update species id');
            assert(state.entry.selectedSuggestion && state.entry.selectedSuggestion.name === 'Species Two', 'selection should update entry selectedSuggestion');

            let renderCalls = 0;
            const oldRender = render;
            render = function () {{ renderCalls += 1; }};
            startNewEntry();

            assert(state.entry.speciesId === 'mushroom-001', 'new entry should reset species id');
            assert(state.entry.selectedSuggestion === null, 'new entry should clear selected suggestion');
            assert(state.analysis.selectedIndex === -1, 'analysis selected index should reset');
            assert(state.analysis.suggestions.length === 0, 'analysis suggestions should reset');
            assert(renderCalls === 1, 'integration should still render once');
            render = oldRender;
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    
    
    
    
    
    
    
    
    
    # 5 Tests added by Sriya
    # AI-ASSISTED TESTS (Course AI Policy)
    #
    # I identified three untouched functions in index.html getSavedCollection, Validator,
    # and queuePhotoForAnalysis and used AI to help generate unit tests for them.
    # Tests cover empty storage handling, data parsing, validation logic, and photo queuing behavior.
    #
    # Prompt used (AI):
    # "Following the same test format, create 5 tests that test the untouched methods
    # getSavedCollection, Validator, and queuePhotoForAnalysis implemented in index.html."

    def test_getSavedCollection_empty_unit(self):
        js = textwrap.dedent(
            """
            const result = getSavedCollection();
            assert(Array.isArray(result), 'should return an array');
            assert(result.length === 0, 'should return empty array when nothing is stored');
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    def test_getSavedCollection_with_data_unit(self):
        js = textwrap.dedent(
            """
            localStorage.setItem('mushroom-log-collection', JSON.stringify([{ savedId: 'test-1', journalName: 'Forest Walk' }]));
            const result = getSavedCollection();
            assert(result.length === 1, 'should return one entry');
            assert(result[0].savedId === 'test-1', 'should parse savedId correctly');
            assert(result[0].journalName === 'Forest Walk', 'should parse journalName correctly');
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    def test_validator_rejects_empty_entry_unit(self):
        js = textwrap.dedent(
            """
            const v = new Validator();
            assert(v.validate({ notes: '', photos: [] }) === false, 'empty notes and no photos should fail validation');
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    def test_validator_accepts_valid_entry_unit(self):
        js = textwrap.dedent(
            """
            const v = new Validator();
            assert(v.validate({ notes: 'Found near oak tree', photos: [] }) === true, 'entry with notes should pass validation');
            assert(v.validate({ notes: '', photos: [{ id: '1' }] }) === true, 'entry with a photo but no notes should also pass');
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)

    def test_queuePhoto_sets_queued_state_unit(self):
        js = textwrap.dedent(
            """
            const photo = { id: 'p1', name: 'mushroom.jpg' };
            queuePhotoForAnalysis(photo);
            assert(photo.analysisState === 'queued', 'analysisState should be set to queued');
            assert(photo.analysisLabel === 'Queued for identification', 'analysisLabel should be set correctly');
            """
        )
        result = run_js_assertions(js)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("JS_ASSERTIONS_OK", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
