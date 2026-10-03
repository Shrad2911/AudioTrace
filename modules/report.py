from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os


def generate_report(
    filepath,
    filename,
    filesize,
    md5,
    sha256,
    metadata,
    audio_results,
    anomaly_results,
    output_path
):

    # -------------------------
    # Create PDF document
    # -------------------------

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    story = []

    # -------------------------
    # Title
    # -------------------------

    story.append(
        Paragraph(
            "AudioTrace",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Digital Forensic Audio Analysis Report",
            heading_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # -------------------------
    # File Information
    # -------------------------

    story.append(
        Paragraph(
            "1. File Information",
            heading_style
        )
    )

    file_data = [
        ["Property", "Value"],
        ["File Name", filename],
        ["File Size", f"{filesize} bytes"]
    ]

    file_table = Table(
        file_data,
        colWidths=[2 * inch, 4 * inch]
    )

    file_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(file_table)

    story.append(Spacer(1, 20))

    # -------------------------
    # File Integrity
    # -------------------------

    story.append(
        Paragraph(
            "2. File Integrity",
            heading_style
        )
    )

    hash_data = [
        ["Hash Type", "Hash Value"],
        ["MD5", md5],
        ["SHA-256", sha256]
    ]

    hash_table = Table(
        hash_data,
        colWidths=[1.5 * inch, 4.5 * inch]
    )

    hash_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("FONTSIZE", (0, 1), (-1, -1), 7)
        ])
    )

    story.append(hash_table)

    story.append(Spacer(1, 20))

    # -------------------------
    # Audio Metadata
    # -------------------------

    story.append(
        Paragraph(
            "3. Audio Metadata",
            heading_style
        )
    )

    metadata_data = [
        ["Property", "Value"],
        ["Format", metadata.get("format", "Unknown")],
        ["Codec", metadata.get("codec", "Unknown")],
        ["Codec Details", metadata.get("codec_long", "Unknown")],
        ["Duration", f"{metadata.get('duration', 'Unknown')} seconds"],
        ["Sample Rate", f"{metadata.get('sample_rate', 'Unknown')} Hz"],
        ["Channels", metadata.get("channels", "Unknown")],
        ["Bitrate", f"{metadata.get('bitrate', 'Unknown')} bits/second"]
    ]

    metadata_table = Table(
        metadata_data,
        colWidths=[2 * inch, 4 * inch]
    )

    metadata_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(metadata_table)

    story.append(Spacer(1, 20))

    # -------------------------
    # Signal Analysis
    # -------------------------

    story.append(
        Paragraph(
            "4. Signal Analysis",
            heading_style
        )
    )

    signal_data = [
        ["Parameter", "Value"],
        [
            "Average RMS Energy",
            audio_results.get("average_rms", "Unknown")
        ],
        [
            "Maximum RMS Energy",
            audio_results.get("maximum_rms", "Unknown")
        ],
        [
            "Average Zero Crossing Rate",
            audio_results.get("average_zcr", "Unknown")
        ]
    ]

    signal_table = Table(
        signal_data,
        colWidths=[3 * inch, 3 * inch]
    )

    signal_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(signal_table)

    story.append(Spacer(1, 20))

    # -------------------------
    # Frequency Analysis
    # -------------------------

    story.append(
        Paragraph(
            "5. Frequency Analysis",
            heading_style
        )
    )

    dominant_frequency = audio_results.get(
        "dominant_frequency",
        "Unknown"
    )

    story.append(
        Paragraph(
            f"<b>Dominant Frequency:</b> "
            f"{dominant_frequency} Hz",
            normal_style
        )
    )

    story.append(Spacer(1, 10))

    frequency_image = audio_results.get(
        "frequency_spectrum"
    )

    if frequency_image and os.path.exists(frequency_image):

        story.append(
            Image(
                frequency_image,
                width=6.5 * inch,
                height=2.6 * inch
            )
        )

    story.append(Spacer(1, 20))

    # -------------------------
    # Anomaly Indicators
    # -------------------------

    story.append(
        Paragraph(
            "6. Potential Anomaly Indicators",
            heading_style
        )
    )

    anomaly_data = [
        ["Indicator", "Value"],
        [
            "Low-Energy / Silence Percentage",
            f"{anomaly_results.get('silence_percentage', 'Unknown')}%"
        ],
        [
            "Energy Variation",
            anomaly_results.get(
                "energy_variation",
                "Unknown"
            )
        ],
        [
            "Sudden Signal Changes",
            anomaly_results.get(
                "sudden_changes",
                "Unknown"
            )
        ]
    ]

    anomaly_table = Table(
        anomaly_data,
        colWidths=[3.5 * inch, 2.5 * inch]
    )

    anomaly_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(anomaly_table)

    story.append(Spacer(1, 15))

    # -------------------------
    # Forensic Findings
    # -------------------------

    story.append(
        Paragraph(
            "Forensic Findings",
            heading_style
        )
    )

    for finding in anomaly_results.get(
        "findings",
        []
    ):

        story.append(
            Paragraph(
                f"• {finding}",
                normal_style
            )
        )

        story.append(
            Spacer(1, 5)
        )

    # story.append(PageBreak())

    # -------------------------
    # Waveform
    # -------------------------

    story.append(
        Paragraph(
            "7. Waveform Analysis",
            heading_style
        )
    )

    waveform_image = audio_results.get(
        "waveform"
    )

    if waveform_image and os.path.exists(waveform_image):

        story.append(
            Image(
                waveform_image,
                width=6.5 * inch,
                height=2.6 * inch
            )
        )

    story.append(Spacer(1, 20))

    # -------------------------
    # Spectrogram
    # -------------------------

    story.append(
        Paragraph(
            "8. Spectrogram Analysis",
            heading_style
        )
    )

    spectrogram_image = audio_results.get(
        "spectrogram"
    )

    if spectrogram_image and os.path.exists(
        spectrogram_image
    ):

        story.append(
            Image(
                spectrogram_image,
                width=6.5 * inch,
                height=2.6 * inch
            )
        )

    story.append(Spacer(1, 20))

    # -------------------------
    # Disclaimer
    # -------------------------

    story.append(
        Paragraph(
            "<b>Forensic Analysis Disclaimer</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "The results generated by AudioTrace represent "
            "potential forensic indicators based on file "
            "integrity, metadata and audio signal analysis. "
            "These results do not independently establish "
            "that an audio file is authentic, edited or fake. "
            "Further forensic examination and comparison "
            "with known-original evidence may be required.",
            normal_style
        )
    )

    # -------------------------
    # Build PDF
    # -------------------------

    document.build(story)