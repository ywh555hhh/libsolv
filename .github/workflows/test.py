from glob import glob
import pip
pip.main(["install", glob("dist/*.whl")[0]])
import solv
pool = solv.Pool()
repo = pool.add_repo("repo")
repodata = repo.add_repodata()
pkg = repo.add_solvable()
pkg.name = 'example'
pkg.evr = "{epoch}:{version}-{release}".format(epoch=0,version="1.0", release="1")
pkg.arch = 'noarch'
pool.createwhatprovides()
pkg.add_deparray(solv.SOLVABLE_PROVIDES, pool.rel2id(pkg.nameid, pkg.evrid, solv.REL_EQ))
pool.createwhatprovides()
jobs1 = pool.select(pkg.name, solv.Selection.SELECTION_PROVIDES).jobs(solv.Job.SOLVER_INSTALL)
print(jobs1)
dirid = repodata.str2dir("/usr/include")
repodata.add_dirstr(pkg.id, solv.SOLVABLE_FILELIST, dirid, "example.h")
repodata.internalize()
pool.addfileprovides()
pool.createwhatprovides()
jobs2 = pool.select("/usr/include/example.h", solv.Selection.SELECTION_FILELIST).jobs(solv.Job.SOLVER_INSTALL)
print(jobs2)
assert (len(jobs1) > 0) and (len(jobs2) > 0)
