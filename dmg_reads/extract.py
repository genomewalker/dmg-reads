from collections import defaultdict
from wsgiref.util import request_uri
import tqdm
import pandas as pd
import pysam
from Bio import SeqIO, Seq, SeqRecord
import logging
import cProfile as profile
import pstats

log = logging.getLogger("my_logger")


def get_read_by_taxa(samfile, refs_tax, refs, refs_damaged):
    prof = profile.Profile()
    prof.enable()
    reads = defaultdict(lambda: defaultdict(dict))

    for reference in tqdm.tqdm(
        refs,
        total=len(refs),
        leave=False,
        desc="References processed",
    ):
        for aln in tqdm.tqdm(
            samfile.fetch(
                reference=reference[0], multiple_iterators=False, until_eof=True
            ),
            total=reference[1],
            ncols=80,
            ascii="░▒█",
            leave=False,
            desc="Alignments processed",
        ):
            # create read
            # Check if reference is damaged
            aln_reference_name = aln.reference_name
            aln_qname = aln.qname
            is_damaged = "non-damaged"
            if aln_reference_name in refs_damaged:
                is_damaged = "damaged"

            if reads[refs_tax[aln_reference_name]][aln_qname]:
                dmg = reads[refs_tax[aln_reference_name]][aln_qname]["is_damaged"]
                if dmg == is_damaged:
                    continue
                else:
                    reads[refs_tax[aln_reference_name]][aln_qname][
                        "is_damaged"
                    ] = "multi"
            else:
                seq = Seq.Seq(aln.seq)
                qual = aln.query_qualities
                if aln.is_reverse:
                    seq = seq.reverse_complement()
                    qual = qual[::-1]
                reads[refs_tax[aln_reference_name]][aln_qname] = {
                    "seq": seq,
                    "qual": qual,
                    "is_damaged": is_damaged,
                }

    prof.disable()
    # print profiling output
    stats = pstats.Stats(prof).strip_dirs().sort_stats("cumtime")
    stats.print_stats(10)  # top 10 rows

    samfile.close()
    return reads
