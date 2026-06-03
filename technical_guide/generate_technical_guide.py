"""
Generate the DSC Analysis Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: dsc_analysis_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "dsc_analysis_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"DSC Analysis — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("DSC Analysis", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Distance Sample Count — Wildlife Survey Analysis Pipeline", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>dsc_analysis</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>dsc_analysis</b> workflow ingests Distance Sample Count (DSC) "
      "wildlife survey data from EarthRanger and produces structured, analysis-ready "
      "datasets for use in population density modelling. The workflow supports "
      "<b>multiple surveys</b> in a single run, each defined by its own EarthRanger "
      "connection, patrol type, survey time window, and transect spatial group."),
    sp(4),
    p("For each configured survey the workflow delivers:"),
    bullet("A <b>metadata CSV</b> — survey-level observations including transect IDs, "
           "observer counts, team members, and event types"),
    bullet("An <b>analysis data CSV</b> — wildlife observation events enriched with "
           "off-transect distances, orthogonal distances, estimated animal positions, "
           "and satellite-derived environmental covariates (NDVI, terrain slope)"),
    bullet("An <b>events GeoPackage</b> — spatial point layer of wildlife observations "
           "with key distance sampling geometry fields"),
    bullet("A <b>transects GeoPackage</b> — visited transect lines labelled with "
           "mean NDVI and slope values from Google Earth Engine"),
    bullet("An <b>original transects GeoPackage</b> — unprocessed transect lines "
           "as fetched from EarthRanger, in EPSG:4326"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Format", "Description"],
            ["{survey}_analysis_metadata", "CSV",
             "Survey event metadata: transect IDs, team members, observer counts, event types"],
            ["{survey}_analysis_data",     "CSV",
             "Wildlife observations with distance fields, animal position estimates, "
             "NDVI, and slope covariates"],
            ["{survey}_events",            "GeoPackage",
             "Spatial point layer of wildlife observation events"],
            ["{survey}_transects",         "GeoPackage",
             "Visited transects with NDVI and slope labels (EPSG:4326)"],
            ["{survey}_orig_transects",    "GeoPackage",
             "Original, unmodified transect lines in EPSG:4326"],
        ],
        [5*cm, 2.5*cm, W - 7.5*cm],
    ),
    note("{survey} is the survey name as defined in the connection configuration. "
         "All five output file sets are produced independently for each survey."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    p("The workflow declares eight versioned packages from the Ecoscope "
      "prefix.dev channels:"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-workflows-core",                "0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope",        "0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",          "0.0.50.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",             "0.0.18.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life",        "0.0.8.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",             "0.0.8.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ate",             "0.0.3.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-distance-sample-counts", "0.0.2.*", "ecoscope-workflows-custom"],
        ],
        [7*cm, 3*cm, W - 10*cm],
    ),
    sp(6),
    h2("2.2  Google Earth Engine connection"),
    p("A Google Earth Engine (GEE) service account connection is required "
      "(<b>set_gee_connection</b>). The GEE client is used to build satellite "
      "imagery composites and label transect lines with environmental covariates. "
      "The same GEE client is shared across all surveys in a single run."),
    sp(6),
    h2("2.3  EarthRanger connections"),
    p("One EarthRanger connection is required <i>per survey</i>. Each entry in "
      "<b>connection_config</b> pairs an EarthRanger server and patrol type ID "
      "with one or more survey definitions (survey name, time window, and "
      "transect spatial group ID). Connections are split and distributed to "
      "parallel per-survey pipelines via <b>split_connection_configs</b>."),
    sp(6),
    h2("2.4  EarthRanger data requirements"),
    p("The workflow expects the following event types to be present in EarthRanger "
      "for each patrol:"),
    make_table(
        [
            ["Event type", "Role"],
            ["distancecountpatrol_rep",        "Survey metadata event — carries transect ID, "
                                               "team members, and observer count"],
            ["distance_count_patrol_metadata", "Alternative metadata event type (also retained "
                                               "during metadata filtering)"],
            ["distancecountwildlife_rep",       "Wildlife observation event — carries species, "
                                               "total count, distance to centre, radial angle, "
                                               "and juvenile count"],
        ],
        [5*cm, W - 5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. INPUT CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Input Configuration"),
    hr(),
    h2("3.1  Workflow-level parameters"),
    make_table(
        [
            ["Parameter", "Description"],
            ["workflow_details",  "Human-readable name and optional description for this "
                                  "workflow run — used for dashboard registration"],
            ["time_range",        "Required on all Ecoscope workflows. Used for timestamp "
                                  "display and UTC conversion only — does not filter which "
                                  "patrol events are fetched. Set broadly to cover all surveys "
                                  "in the run. Each survey's own time window controls data fetching."],
            ["gee_client",        "Google Earth Engine service account connection"],
            ["connection_config", "Array of EarthRanger connection entries, one per survey "
                                  "(see Section 3.2)"],
        ],
        [4*cm, W - 4*cm],
    ),
    sp(6),
    h2("3.2  Connection config entry (per survey)"),
    p("Each entry in <b>connection_config</b> defines one EarthRanger site and "
      "one or more surveys to run against it:"),
    make_table(
        [
            ["Field", "Type", "Description"],
            ["earthranger.server",     "Connection", "EarthRanger data source connection"],
            ["earthranger.patrol_type_id", "String",
             "Numeric or UUID identifier for the patrol type containing DSC surveys"],
            ["surveys[].surveyName",   "String",  "Unique name for this survey (used as output filename prefix)"],
            ["surveys[].time_range",   "Object",  "Survey-specific data fetch window. Patrol events within this "
                                                  "since / until range are retrieved from EarthRanger for this "
                                                  "survey. This is the field that controls which data is pulled — "
                                                  "not the top-level time_range."],
            ["surveys[].erSpatialTransectsGroupId", "String",
             "EarthRanger spatial group ID that contains the transect line features"],
        ],
        [4*cm, 2*cm, W - 6*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. DATA INGESTION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Data Ingestion"),
    hr(),
    h2("4.1  Connection splitting"),
    p("The combined <b>connection_config</b> is split into individual "
      "per-survey connection objects via <b>split_connection_configs</b>. "
      "All subsequent steps that require per-survey data use "
      "<b>mapvalues</b> to fan out over this list in parallel."),
    sp(6),
    h2("4.2  Patrol events"),
    p("For each survey, <b>fetch_patrol_events</b> retrieves all patrols matching "
      "the configured patrol type ID within the survey time window. "
      "The resulting patrol DataFrame is indexed on the <b>id</b> column via "
      "<b>set_dataframe_index</b> to enable subsequent join operations."),
    sp(6),
    h2("4.3  Patrol transects"),
    p("Transect lines are fetched in parallel with patrol events via "
      "<b>fetch_transects</b>, using the spatial group ID specified in each "
      "survey's connection config. The transects are GeoDataFrames in EPSG:4326 "
      "as returned by EarthRanger."),
    sp(6),
    h2("4.4  Survey observation events"),
    p("Individual wildlife observation events are fetched from the patrol event IDs "
      "returned by <b>fetch_patrol_events</b> using <b>fetch_events</b> "
      "(chunk_size: 50). This two-step approach — fetch patrols first, then fetch "
      "the events within them — is required because the EarthRanger API does not "
      "support direct patrol-type filtering on the events endpoint."),
    sp(6),
    h2("4.5  EarthRanger server name"),
    p("The EarthRanger server name (site identifier) is retrieved per survey via "
      "<b>get_server_name</b> and zipped with the survey event DataFrame. It is "
      "passed to <b>process_events_details</b> as the <b>client</b> argument so "
      "that EarthRanger field IDs can be resolved to human-readable display names."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. EVENT PROCESSING PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Event Processing Pipeline"),
    hr(),
    h2("5.1  Metadata event branch"),
    p("Survey metadata events (<b>distancecountpatrol_rep</b> and "
      "<b>distance_count_patrol_metadata</b>) are processed through a dedicated "
      "branch to produce the <i>analysis metadata</i> output:"),
    make_table(
        [
            ["Step", "Task", "Purpose"],
            ["1", "filter_row_values",
             "Retain only metadata event types from the raw event fetch"],
            ["2", "parse_df_point",
             "Extract latitude and longitude columns from the GeoDataFrame geometry"],
            ["3", "normalize_json_column (reported_by)",
             "Flatten the reported_by JSON field into flat columns"],
            ["4", "join_list_column (reported_by__name)",
             "Collapse list values in reported_by__name to a comma-separated string"],
            ["5", "process_events_details",
             "Resolve EarthRanger field IDs to display names "
             "(map_to_titles: true, ordered: true)"],
            ["6", "normalize_json_column (event_details)",
             "Flatten the event_details JSON into flat columns"],
            ["7", "map_columns",
             "Retain and rename key columns: time, event_type, serial_number, "
             "latitude, longitude, reported_by, Transect ID, Team Members, "
             "Number of Observers"],
            ["8", "parse_list_column / join_list_column (Team Members)",
             "Parse and flatten Team Members list into a comma-separated string"],
            ["9", "drop_null_columns",
             "Drop any columns that are entirely null after normalisation"],
        ],
        [1.5*cm, 4.5*cm, W - 6*cm],
    ),
    p("The resulting DataFrame is persisted as "
      "<b>{survey_name}_analysis_metadata.csv</b>."),
    sp(6),
    h2("5.2  Wildlife observation event branch"),
    p("Wildlife observation events (<b>distancecountwildlife_rep</b>) pass through "
      "a separate normalisation branch before being merged with patrol-level "
      "metadata:"),
    make_table(
        [
            ["Step", "Task", "Purpose"],
            ["1", "select_columns (event_details)",
             "Extract only the event_details column from the raw event fetch "
             "for merging with the patrol DataFrame"],
            ["2", "merge_two_dataframes (left join on index)",
             "Join the patrol DataFrame with the event_details column using "
             "the patrol id index"],
            ["3", "convert_column_timezone",
             "Convert the time column to UTC using the timezone from the global time_range "
             "(used for display/conversion only, not for data filtering)"],
            ["4", "normalize_json_column (event_details)",
             "Flatten the merged event_details JSON into flat columns"],
            ["5", "map_columns (patrol rename)",
             "Rename flattened distance sampling fields to standardised names "
             "(see table below)"],
            ["6", "bfill_within_patrols / ffill_within_patrols",
             "Backward- then forward-fill transect_id and num_observers "
             "within each patrol (group_col: patrol_serial_number) to propagate "
             "metadata event values to wildlife observation rows"],
            ["7", "filter_row_values (distancecountwildlife_rep)",
             "Retain only wildlife observation events after fill propagation"],
            ["8", "add_constant_column (survey_id)",
             "Stamp each row with the survey name as a survey_id identifier"],
        ],
        [1.5*cm, 4.5*cm, W - 6*cm],
    ),
    sp(6),
    h2("5.3  Field name mapping"),
    p("The <b>map_columns</b> step in the wildlife observation branch renames "
      "the flattened EarthRanger field codes to analysis-ready column names:"),
    make_table(
        [
            ["Source field (EarthRanger)", "Target column"],
            ["event_details__distancecountpatrol_numberofobservers", "num_observers"],
            ["event_details__distancecountpatrol_teammembers",        "Team Members"],
            ["event_details__distancecountpatrol_transectid",         "transect_id"],
            ["event_details__distancecountwildlife_distancetocentre", "dist_to_centre"],
            ["event_details__distancecountwildlife_numberofjuveniles","num_juveniles"],
            ["event_details__distancecountwildlife_radialangle",       "radialangle"],
            ["event_details__distancecountwildlife_species",           "species"],
            ["event_details__distancecountwildlife_totalcount",        "totalcount"],
            ["event_details__Transect_ID  (alt. form)",               "transect_id"],
            ["event_details__Team_members (alt. form)",                "Team Members"],
            ["event_details__Number_of_observers (alt. form)",         "num_observers"],
        ],
        [8*cm, W - 8*cm],
    ),
    note("The mapping includes both the snake_case EarthRanger internal names and "
         "alternative title-case forms to handle variation across EarthRanger "
         "server configurations. raise_if_not_found is set to false so that "
         "missing columns are silently ignored."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. TRANSECT PROCESSING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Transect Processing"),
    hr(),
    h2("6.1  CRS conversion to UTM"),
    p("Distance sampling calculations require a metric coordinate reference system. "
      "The UTM zone is estimated automatically from the transect geometry via "
      "<b>estimate_utm_crs</b>. Both the transect GeoDataFrame and the wildlife "
      "observation GeoDataFrame are then reprojected to this UTM CRS via "
      "<b>reproject_gdf</b> before any distance calculations are performed."),
    sp(6),
    h2("6.2  Transect simplification and buffering"),
    p("Before spatial intersection tests, the transect lines are prepared as follows:"),
    make_table(
        [
            ["Step", "Task", "Parameters", "Purpose"],
            ["1", "merge_transect_lines", "—",
             "Merge all transect line segments for the survey into a unified "
             "GeoDataFrame keyed by transect name"],
            ["2", "simplify_transects", "tolerance: 50 m",
             "Reduce transect vertex count while preserving shape — "
             "improves intersection performance"],
            ["3", "buffer_transects",
             "distance: 500 m, cap_style: flat, single_sided: false, resolution: 5",
             "Create a 500 m bilateral corridor around each transect for "
             "event intersection testing"],
        ],
        [1.5*cm, 4*cm, 4*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("6.3  Event–transect intersection filter"),
    p("Wildlife observation events are tested against the buffered transect corridors "
      "via <b>flag_events_intersecting_transect</b>. This step adds an "
      "<b>intersects_transect</b> boolean column and records which transect each "
      "event falls within (transect_id_column: transect_id, "
      "transect_name_column: name, index_column: id)."),
    sp(4),
    p("Only transects visited by at least one intersecting event are retained for "
      "the final output via <b>filter_visited_transects</b>. This removes "
      "transects that were planned but not walked during the survey period."),
    sp(6),
    h2("6.4  Re-projection to EPSG:4326 for export"),
    p("After intersection filtering, visited transects are reprojected back to "
      "EPSG:4326 (<b>reproject_gdf</b>, target_crs: \"epsg:4326\") before "
      "satellite imagery labeling and GeoPackage export."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. GEOMETRIC CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Geometric Calculations"),
    hr(),
    h2("7.1  Off-transect distance (observer position)"),
    p("The perpendicular distance from the <i>observer's recorded GPS position</i> "
      "to the nearest transect centreline is calculated via "
      "<b>add_off_transect_distance</b> and stored in the column "
      "<b>off_transect_dist</b>. Events where the computed distance equals "
      "<b>−1</b> (indicating that no matching transect was found) are removed "
      "via <b>filter_numeric_df</b> (op: \"ne\", value: −1)."),
    sp(6),
    h2("7.2  Estimated animal position"),
    p("The true animal position is estimated from the observer position, the "
      "recorded radial angle (<b>radialangle</b>), and the recorded distance "
      "from observer to detected animal (<b>dist_to_centre</b>) via "
      "<b>estimate_animal_positions</b>. The original observer geometry is "
      "preserved first by <b>add_orig_geometry</b> into the column "
      "<b>orig_geometry</b>; the main geometry column is then replaced with "
      "the estimated animal position."),
    sp(6),
    h2("7.3  Orthogonal distance (animal position)"),
    p("After the animal position is estimated, the perpendicular distance from "
      "the <i>estimated animal position</i> to the transect centreline is "
      "computed via a second call to <b>add_off_transect_distance</b> and "
      "stored as <b>ortho_dist</b>. This is the key detection distance used "
      "in distance sampling density estimation models."),
    sp(4),
    p("Events with ortho_dist == −1 are again removed via "
      "<b>filter_numeric_df</b> before the data proceeds to imagery labeling."),
    sp(6),
    h2("7.4  Distance calculation summary"),
    make_table(
        [
            ["Column", "Task", "Geometry used", "Meaning"],
            ["off_transect_dist", "add_off_transect_distance (1st call)",
             "Observer GPS position",
             "Distance from observer to transect centreline — QA check"],
            ["orig_geometry",     "add_orig_geometry",
             "Observer GPS position",
             "Preserved original observer geometry before position estimation"],
            ["geometry",          "estimate_animal_positions",
             "Computed from radialangle + dist_to_centre",
             "Estimated true animal location"],
            ["ortho_dist",        "add_off_transect_distance (2nd call)",
             "Estimated animal position",
             "Perpendicular distance from animal to transect — used in DSC models"],
        ],
        [3*cm, 4*cm, 4*cm, W - 11*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. SATELLITE IMAGERY LABELING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Satellite Imagery Labeling"),
    hr(),
    p("Each transect line is labelled with two satellite-derived environmental "
      "covariates using Google Earth Engine. These covariates are commonly used "
      "as predictors in distance sampling detection function models."),
    sp(6),
    h2("8.1  HLS NDVI"),
    p("A Harmonized Landsat Sentinel-2 (HLS) NDVI composite is built per survey "
      "via <b>build_hls_ndvi_image</b>:"),
    make_table(
        [
            ["Parameter", "Value", "Notes"],
            ["ndvi_window_days", "null",
             "No fixed window — uses the full image archive available "
             "up to the survey start date"],
            ["max_cloud_cover",  "30 %",
             "Scenes with more than 30 % cloud cover are excluded from the composite"],
            ["ndvi_band_name",   "NDVI_HSL",
             "Output band name stored in the labelled transect column"],
        ],
        [4*cm, 2.5*cm, W - 6.5*cm],
    ),
    sp(4),
    p("The NDVI image is evaluated over each transect's geometry and the mean "
      "pixel value within each transect is computed via "
      "<b>label_features_with_image_stat</b> (scale: 30 m, reducer_key: mean, "
      "out_column: NDVI_HSL). The survey start date is added as a "
      "<b>img_date_hsl_ndvi</b> column for traceability."),
    sp(6),
    h2("8.2  Terrain slope"),
    p("A slope layer is derived from the USGS SRTM 1-arc-second DEM "
      "(<b>USGS/SRTMGL1_003</b>) via <b>build_slope_image</b>. The mean slope "
      "value within each transect is then computed via a second call to "
      "<b>label_features_with_image_stat</b> (scale: 30 m, reducer_key: mean, "
      "out_column: slope)."),
    sp(6),
    h2("8.3  Imagery labeling workflow"),
    p("The transects are converted to a Google Earth Engine FeatureCollection "
      "via <b>to_ee_feature_collection</b> before labeling. The survey start "
      "date (<b>get_since_filter</b>) is both added as a column to the transect "
      "DataFrame and passed to the NDVI image builder as the <b>since</b> "
      "parameter to anchor the composite date."),
    sp(6),
    h2("8.4  Final transect column selection"),
    p("After labeling, transects are trimmed to the columns required for "
      "merging and export:"),
    make_table(
        [
            ["Column", "Included in GeoPackage", "Included in merge", "Description"],
            ["name",             "Yes", "Yes", "Transect identifier (matches transect_id in patrol events)"],
            ["img_date_hsl_ndvi","Yes", "Yes", "Survey start date used as NDVI image anchor"],
            ["NDVI_HSL",         "Yes", "Yes", "Mean HLS NDVI value along transect"],
            ["slope",            "Yes", "Yes", "Mean terrain slope along transect"],
            ["geometry",         "Yes", "No",  "Transect line geometry (excluded from CSV merge)"],
        ],
        [3.5*cm, 3*cm, 2.5*cm, W - 9*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Output Files"),
    hr(),
    p("All outputs are written to <b>$ECOSCOPE_WORKFLOWS_RESULTS</b>. "
      "Five file sets are produced for each configured survey. "
      "{survey} is replaced with the survey name defined in the connection config."),
    sp(6),
    make_table(
        [
            ["File", "Format", "Description"],
            ["{survey}_analysis_metadata.csv", "CSV",
             "Survey metadata events: transect IDs, team members, observer counts, "
             "event types, lat/lon"],
            ["{survey}_analysis_data.csv", "CSV",
             "Wildlife observation events with all distance sampling fields: "
             "species, totalcount, num_juveniles, dist_to_centre, radialangle, "
             "off_transect_dist, ortho_dist, survey_id, orig_geometry (WKT), "
             "estimated geometry (WKT), NDVI_HSL, slope, img_date_hsl_ndvi, "
             "intersects_transect, transect_id, num_observers, time, "
             "serial_number, patrol_id, patrol_serial_number"],
            ["{survey}_events.gpkg", "GeoPackage",
             "Spatial point layer of wildlife observations. Columns: serial_number, "
             "transect_id, dist_to_centre, ortho_dist, intersects_transect, geometry"],
            ["{survey}_transects.gpkg", "GeoPackage",
             "Visited transect lines (EPSG:4326) with environmental covariates: "
             "name, img_date_hsl_ndvi, NDVI_HSL, slope, geometry"],
            ["{survey}_orig_transects.gpkg", "GeoPackage",
             "Original unprocessed transect lines as fetched from EarthRanger "
             "(EPSG:4326). Includes all fields returned by the EarthRanger spatial "
             "group endpoint"],
        ],
        [5*cm, 2.5*cm, W - 7.5*cm],
    ),
    sp(6),
    note("The _events GeoPackage contains a subset of columns optimised for "
         "spatial QA and GIS workflows. The _analysis_data CSV contains the full "
         "column set including all covariates and is the primary input for "
         "distance sampling density estimation models."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Workflow Execution Logic"),
    hr(),
    h2("10.1  Skip conditions"),
    p("All tasks share a global default skip policy defined in "
      "<b>task-instance-defaults</b>:"),
    bullet("<b>any_is_empty_df</b> — skips the task if any upstream DataFrame "
           "dependency is empty"),
    bullet("<b>any_dependency_skipped</b> — skips the task if any upstream "
           "task was itself skipped"),
    p("This means that if a survey returns no patrol events or no transects, "
      "all downstream tasks for that survey branch are skipped gracefully "
      "without raising an error."),
    sp(6),
    h2("10.2  Per-survey fan-out with mapvalues"),
    p("Every data-bearing step is executed once per survey via the "
      "<b>mapvalues</b> directive. The fan-out list originates from "
      "<b>split_connection_configs</b> and flows through all subsequent "
      "steps. Key fan-out points:"),
    make_table(
        [
            ["Step", "mapvalues source"],
            ["fetch_patrol_events",       "split_connection_config.return"],
            ["fetch_patrol_transects",    "split_connection_config.return"],
            ["fetch_events_from_ids",     "zip_conn_patrol_events.return"],
            ["All event processing steps","Chained from fetch_events_from_ids"],
            ["Transect CRS / distance steps", "Chained from fetch_patrol_transects"],
            ["GEE labeling steps",        "Chained from reproject_transects"],
            ["All persist steps",         "Chained via zip_filename_* groupbykey"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("10.3  zip_groupbykey — multi-input coordination"),
    p("<b>zip_groupbykey</b> is used throughout the workflow to combine two "
      "per-survey lists into paired tuples before feeding them into a two-argument "
      "mapvalues step. Key uses:"),
    bullet("<b>zip_conn_patrol_events</b> — pairs split_connection_config with "
           "set_patrol_index to feed fetch_events_from_ids"),
    bullet("<b>zip_conn_survey_df</b> — pairs the event DataFrame with the "
           "EarthRanger server name to feed process_events_details"),
    bullet("<b>zip_patrol_transects</b> — pairs patrol events (UTM) with transects "
           "(UTM) to feed add_off_transect_distance"),
    bullet("<b>zip_aoi_since</b> — pairs the EE FeatureCollection with the since "
           "date to feed build_hls_ndvi_image"),
    bullet("<b>zip_filename_*</b> — pairs dynamically constructed filename prefixes "
           "with DataFrames to feed persist_df_wrapper"),
    sp(6),
    h2("10.4  Dynamic filename construction"),
    p("Output filenames are constructed at runtime from the survey name "
      "using <b>combine_names</b> with a fixed suffix:"),
    make_table(
        [
            ["Suffix", "Output file purpose"],
            ["_analysis_metadata", "Metadata events CSV"],
            ["_analysis_data",     "Wildlife observations CSV"],
            ["_events",            "Events GeoPackage"],
            ["_transects",         "Visited transects GeoPackage"],
            ["_orig_transects",    "Original transects GeoPackage"],
        ],
        [4*cm, W - 4*cm],
    ),
    sp(6),
    h2("10.5  Fill propagation for metadata fields"),
    p("Patrol events in EarthRanger are recorded sequentially: a metadata event "
      "(distancecountpatrol_rep) carrying the transect ID and observer count "
      "typically appears once per transect walk, while multiple wildlife "
      "observation events (distancecountwildlife_rep) follow it. Because "
      "both event types share the same patrol_serial_number, the workflow "
      "uses backward fill (<b>bfill_within_patrols</b>) followed by forward "
      "fill (<b>ffill_within_patrols</b>) to propagate the transect_id and "
      "num_observers values to every row within the patrol before "
      "filtering to wildlife observation events only."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned"],
            ["ecoscope-workflows-core",                "0.22.17.*"],
            ["ecoscope-workflows-ext-ecoscope",        "0.22.17.*"],
            ["ecoscope-workflows-ext-custom",          "0.0.50.*"],
            ["ecoscope-workflows-ext-ste",             "0.0.18.*"],
            ["ecoscope-workflows-ext-big-life",        "0.0.8.*"],
            ["ecoscope-workflows-ext-mnc",             "0.0.8.*"],
            ["ecoscope-workflows-ext-ate",             "0.0.3.*"],
            ["ecoscope-workflows-ext-distance-sample-counts", "0.0.2.*"],
        ],
        [8*cm, W - 8*cm],
    ),
    sp(6),
    note("All packages are resolved from the prefix.dev Ecoscope conda channels. "
         "The wildcard patch-version pin (.*) allows bug-fix releases to be "
         "picked up automatically while keeping minor and major versions locked."),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Written → {OUTPUT_FILE}")
