# KUKA Arc Welding OLP Guides

These guides describe the KUKA-specific Arc Welding workflow in FASTSUITE E2 for application engineers and E2 administrators. They cover TouchSense, SeamTech Finding, SeamTech Tracking, and native or KUKA ArcTech Multilayer output.

General E2 OLP training, robot mastering, cell commissioning, and the KUKA option packages themselves are outside the scope. Use the relevant KUKA manual for controller operation, safety, mastering, and option-package internals.

## Choose a guide

| Goal | Guide |
| --- | --- |
| Program, simulate, and download sensing, tracking, or Multilayer operations | [OLP Programmer Guide](olp-programmer-guide.md) |
| Install and configure the E2 technology and project-specific mappings | [E2 Administrator Guide](e2-admin-guide.md) |
| Look up attributes, JSON mappings, generated KRL, and diagnostic codes | [Configuration Reference](configuration-reference.md) |
| Diagnose output, controller-load, correction, or recipe problems | [Troubleshooting and Validation](troubleshooting-validation.md) |

## Capability and validation status

These guides describe maintained customization workflows; they do not certify a particular cell or option-package combination. Validate each target configuration using its own controller, project data, and commissioning process before release.

## Source material

The guides summarize the E2 workflow and link to the licensed KUKA references instead of reproducing them:

- [KUKA.TouchSense 3.2.2 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB12250_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.TouchSense%203.2.2%20manual%22%2C%22page%22%3A32%7D)
- [KUKA.SeamTech Finding 4.0.3 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB22249_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.SeamTech%20Finding%204.0.3%20manual%22%2C%22page%22%3A39%7D)
- [KUKA.SeamTech Tracking 4.0.3 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB21432_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.SeamTech%20Finding%204.0.3%20manual%22%2C%22page%22%3A39%7D)
- [KUKA.ArcTech Multilayer 3.7.1 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB22944_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.ArcTech%20Multilayer%203.7.1%20manual%22%2C%22page%22%3A35%7D)

Cell-specific generated programs, screenshots, and recordings are intentionally not included. Generate and validate output in the target E2 project.

## Terms used in these guides

| Term | Meaning |
| --- | --- |
| E2 native paths | Every Multilayer pass is a complete, independently generated E2 path |
| AML | KUKA ArcTech Multilayer output; the root geometry is recorded and filler positions are derived on the controller |
| Root pass | The first ordered pass of a Multilayer seam and the sensing owner for that seam |
| Seam frame | Local correction frame with X along the seam, Z opposite the welding tool Z direction, and Y completing the right-handed frame |
| Sensor dataset | Controller-side TouchSense, Finding, or Tracking data referenced by an E2 sensor ID, task, set, or correction ID |

## Safety boundary

Always validate generated SRC/DAT in the target controller environment, perform a dry run at reduced speed, and complete the applicable KUKA safety and option-package commissioning procedures. E2 collision-free simulation does not prove that sensor search limits, correction signs, process data, or controller-generated AML filler paths are safe on the real cell.
