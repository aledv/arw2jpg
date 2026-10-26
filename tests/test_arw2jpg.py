"""Unit tests for the arw2jpg CLI (conversion itself is mocked: no RAW samples needed)."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from arw2jpg import arw2jpg as cli


class Arw2JpgTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for name in ("b.ARW", "a.arw", "c.NEF", "notes.txt"):
            (self.tmp / name).write_bytes(b"x")
        (self.tmp / "sub").mkdir()
        (self.tmp / "sub" / "d.ARW").write_bytes(b"x")

    def test_find_is_case_insensitive_sorted_and_not_recursive(self):
        self.assertEqual([p.name for p in cli.find_raw_files(self.tmp)], ["a.arw", "b.ARW"])
        self.assertEqual([p.name for p in cli.find_raw_files(self.tmp, ["arw", ".nef"])], ["a.arw", "b.ARW", "c.NEF"])

    def test_output_path(self):
        self.assertEqual(cli.output_path(Path("/p/DSC001.ARW"), Path("/out")), Path("/out/DSC001.jpg"))

    def test_folder_without_trailing_slash_and_options_before_it(self):
        with mock.patch.object(cli, "convert", side_effect=lambda job: job[1]) as convert:
            self.assertEqual(cli.main(["-n", "1", "-q", "80", str(self.tmp)]), 0)
        jobs = [c.args[0] for c in convert.call_args_list]
        self.assertEqual([j[1] for j in jobs], [self.tmp / "converted" / "a.jpg", self.tmp / "converted" / "b.jpg"])
        self.assertTrue(all(j[2] == 80 for j in jobs))
        self.assertTrue((self.tmp / "converted").is_dir())

    def test_existing_jpegs_skipped_unless_overwrite(self):
        out = self.tmp / "out"
        out.mkdir()
        (out / "a.jpg").write_bytes(b"done")
        with mock.patch.object(cli, "convert", side_effect=lambda job: job[1]) as convert:
            cli.main(["-n", "1", "-o", str(out), str(self.tmp)])
            self.assertEqual([c.args[0][0].name for c in convert.call_args_list], ["b.ARW"])
            convert.reset_mock()
            cli.main(["-n", "1", "-f", "-o", str(out), str(self.tmp)])
            self.assertEqual(convert.call_count, 2)

    def test_invalid_arguments(self):
        for argv in (["-q", "0", "x"], ["-n", "0", "x"]):
            with self.assertRaises(SystemExit), mock.patch("sys.stderr"):
                cli.parse_args(argv)
        with mock.patch("sys.stderr"):
            self.assertEqual(cli.main([str(self.tmp / "missing")]), 2)

    def test_default_cores_never_zero(self):
        with mock.patch.object(cli.mp, "cpu_count", return_value=1):
            self.assertEqual(cli.parse_args(["x"]).numb_cores, 1)


if __name__ == "__main__":
    unittest.main()
