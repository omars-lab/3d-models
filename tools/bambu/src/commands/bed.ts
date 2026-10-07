// `bambu bed` — the bed photo a send rests on, and what someone saw in it.
//   photo <plate>   : one camera frame of the bed, saved under .bambu/bed/ (read-only camera)
//   show <plate>    : the newest photo of that plate, its age, and its verdict
//   verdict <plate> : write down what the newest photo shows; `print send` refuses without it
//
// Why the verdict exists, and what the send checks against it: bed-check.ts.

import { Command } from "commander";
import { mkdirSync } from "node:fs";
import { basename, join } from "node:path";
import { CameraBackend } from "../backends/camera.js";
import { loadConfig, type PrinterConfig } from "../config.js";
import { repoRoot } from "../paths.js";
import { parsePlateTypeFlag } from "../plate-type.js";
import { plateNameOf } from "../send-gate.js";
import { bedDir, bedPhotoName, newestBedPhoto, plateKind, readVerdict, writeVerdict } from "../bed-check.js";

const root = (): string => repoRoot() ?? process.cwd();

/** Save one camera frame of the bed for this plate and say where; warn and return null if it fails. */
export async function bedPhoto(plate: string, cfg: PrinterConfig): Promise<string | null> {
  const out = join(bedDir(root()), bedPhotoName(plate));
  mkdirSync(bedDir(root()), { recursive: true });
  try {
    await new CameraBackend(cfg).snapshot(out);
    console.error(`bed photo: ${out} — open it, then record what it shows: bambu bed verdict ${plate} …`);
    return out;
  } catch (err) {
    console.error(`bed photo: none (${(err as Error).message}) — the send needs one with a verdict.`);
    return null;
  }
}

interface VerdictOpts {
  clear?: boolean;
  seated?: boolean;
  plateType: string;
  nonBambu?: boolean;
  bambuPlate?: boolean;
  by: string;
  note?: string;
}

export function registerBed(program: Command): void {
  const bed = program.command("bed").description("the bed photo a send rests on, and the written verdict on it");

  bed
    .command("photo")
    .description("take one photo of the bed for a plate (read-only camera); look at it, then `bed verdict`")
    .argument("<plate>", "plate name or its .3mf, e.g. sheets-04b")
    .action(async (plate: string) => {
      const shot = await bedPhoto(plateNameOf(plate), loadConfig());
      if (!shot) process.exitCode = 1;
    });

  bed
    .command("show")
    .description("the newest bed photo of a plate, how old it is, and its verdict")
    .argument("<plate>", "plate name or its .3mf")
    .action((plate: string) => {
      const name = plateNameOf(plate);
      const photo = newestBedPhoto(root(), name);
      if (!photo) {
        console.log(`no bed photo of ${name} under ${bedDir(root())}`);
        return;
      }
      const ageMin = Math.floor((Date.now() - photo.mtimeMs) / 60000);
      console.log(`${photo.path} (${ageMin} min old)`);
      const v = readVerdict(photo.path);
      if (!v) console.log("verdict: none yet");
      else if (v.sha256 !== photo.sha256) console.log("verdict: for other photo bytes — look again");
      else {
        console.log(
          `verdict: ${v.bed_clear ? "clear" : "NOT clear"}, ${v.plate_seated ? "plate seated" : "plate NOT seated"}, ` +
            `${v.plate_type} (${plateKind(v)}), by ${v.by} at ${v.at}${v.note ? ` — ${v.note}` : ""}`,
        );
      }
    });

  bed
    .command("verdict")
    .description("write down what the newest bed photo of a plate shows, after opening it")
    .argument("<plate>", "plate name or its .3mf")
    .requiredOption("--plate-type <token>", "the plate in the photo: cool_plate, eng_plate, hot_plate, textured_plate, supertack_plate")
    .requiredOption("--by <who>", 'who looked, e.g. "Claude, opened the photo"')
    .option("--clear", "nothing is on the bed")
    .option("--no-clear", "something is on the bed")
    .option("--seated", "the build plate is in and flat")
    .option("--no-seated", "the build plate is missing or not flat")
    .option("--note <text>", "what else the photo shows")
    .option("--bambu-plate", "the plate is Bambu's own (the gold Textured PEI): `options for-bed` keeps its two checks on")
    .option("--non-bambu", "the plate is not Bambu's own (the glacier): `options for-bed` then switches its two checks off")
    .action((plate: string, opts: VerdictOpts) => {
      const name = plateNameOf(plate);
      if (opts.clear === undefined || opts.seated === undefined) {
        console.error("say both: --clear or --no-clear, and --seated or --no-seated.");
        process.exitCode = 2;
        return;
      }
      // Both plates read P0101, so only the look can say which it is; a verdict that is silent on it
      // once set the glacier's checks for a Bambu plate.
      if (opts.bambuPlate === opts.nonBambu) {
        console.error("say which plate it is: --bambu-plate (Bambu's own) or --non-bambu (the glacier).");
        process.exitCode = 2;
        return;
      }
      let token: string;
      try {
        token = parsePlateTypeFlag(opts.plateType).token;
      } catch (err) {
        console.error((err as Error).message);
        process.exitCode = 2;
        return;
      }
      const photo = newestBedPhoto(root(), name);
      if (!photo) {
        console.error(`no bed photo of ${name} to judge. Take one: bambu bed photo ${name}`);
        process.exitCode = 2;
        return;
      }
      writeVerdict(photo, {
        plate: name,
        bed_clear: opts.clear,
        plate_seated: opts.seated,
        plate_type: token,
        non_bambu: opts.nonBambu === true,
        by: opts.by,
        ...(opts.note ? { note: opts.note } : {}),
        at: new Date().toISOString(),
      });
      console.log(`verdict written for ${basename(photo.path)}: ${opts.clear ? "clear" : "NOT clear"}, ${opts.seated ? "seated" : "NOT seated"}, ${token}, ${opts.nonBambu ? "not a Bambu plate" : "a Bambu plate"}`);
    });
}
