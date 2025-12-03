╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          🚨 GETTING ARCHITECTURE ERRORS? 🚨                   ║
║                                                               ║
║     (ImportError: incompatible architecture x86_64/arm64)    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

You have MIXED architecture packages (ARM64 + x86_64 conflict).

═══════════════════════════════════════════════════════════════

              ✅ THE DEFINITIVE FIX ✅

═══════════════════════════════════════════════════════════════

Run this ONE command:

    bash fix_architecture.sh

This will:
  ✓ Create clean virtual environment
  ✓ Install all packages with matching architecture
  ✓ Test the installation
  ✓ Create activation helper

Time: 5-10 minutes (downloads packages)

═══════════════════════════════════════════════════════════════

             THEN TO TRAIN YOUR MODEL:

═══════════════════════════════════════════════════════════════

1. Activate environment:
   source venv/bin/activate

2. Train:
   bash train.sh

3. Done! Your model: models/hey_mel.tflite

═══════════════════════════════════════════════════════════════

           EVERY TIME YOU WORK ON THIS:

═══════════════════════════════════════════════════════════════

Always activate the virtual environment first:

    source venv/bin/activate

Or use the helper:

    source activate.sh

═══════════════════════════════════════════════════════════════

              NEED MORE HELP?

═══════════════════════════════════════════════════════════════

Read:   ARCHITECTURE_FIX.md    (detailed explanation)
Read:   TROUBLESHOOTING.md     (common issues)
Read:   START_HERE.md          (general getting started)

═══════════════════════════════════════════════════════════════

